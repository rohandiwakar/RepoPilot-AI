import asyncio
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_settings


class LLMService:
    """Service for interacting with Gemini LLM via LangChain."""

    def __init__(self):
        settings = get_settings()
        self.max_retries = settings.LLM_MAX_RETRIES
        self.retry_base_seconds = settings.LLM_RETRY_BASE_SECONDS
        self.retry_max_seconds = settings.LLM_RETRY_MAX_SECONDS
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,
            max_output_tokens=8192,
        )

    @staticmethod
    def format_provider_error(error: Exception) -> str:
        """Return a concise, user-safe message for common LLM provider failures."""
        message = str(error)
        if "RESOURCE_EXHAUSTED" in message or "429" in message:
            if "GenerateRequestsPerDayPerProjectPerModel-FreeTier" in message:
                return (
                    "Gemini daily free-tier quota was exceeded for this model. "
                    "Wait for the quota reset, enable billing, or set GEMINI_MODEL to a model with available quota."
                )
            return "Gemini rate limit was reached. Please retry after a short wait or use a model with available quota."
        if "API_KEY_INVALID" in message or "API Key not found" in message:
            return "Gemini API key is missing or invalid. Update GEMINI_API_KEY in the backend environment."
        return message

    @staticmethod
    def _retry_delay_from_error(error: Exception) -> float | None:
        match = re.search(r"retryDelay['\"]?:\s*['\"]?(\d+(?:\.\d+)?)s", str(error))
        if match:
            return float(match.group(1))
        return None

    @staticmethod
    def _is_daily_quota_error(error: Exception) -> bool:
        return "GenerateRequestsPerDayPerProjectPerModel-FreeTier" in str(error)

    async def _invoke_with_retry(self, chain, payload: dict) -> str:
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                return await chain.ainvoke(payload)
            except Exception as error:
                last_error = error
                message = str(error)
                retryable = ("RESOURCE_EXHAUSTED" in message or "429" in message) and not self._is_daily_quota_error(error)
                if not retryable or attempt >= self.max_retries:
                    raise RuntimeError(self.format_provider_error(error)) from error

                provider_delay = self._retry_delay_from_error(error)
                fallback_delay = self.retry_base_seconds * (2 ** attempt)
                delay = min(provider_delay or fallback_delay, self.retry_max_seconds)
                await asyncio.sleep(delay)

        raise RuntimeError(self.format_provider_error(last_error))

    async def analyze_project(self, repo_data: dict) -> dict:
        """Analyze the repository data and produce a project summary."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert software architect and technical analyst.
Analyze the GitHub repository data provided and produce a detailed project analysis.
You MUST respond with valid JSON only. No markdown, no explanation outside JSON."""),
            ("human", """Analyze this GitHub repository:

Repository: {repo_url}
Name: {name}
Description: {description}
Primary Language: {language}
Languages: {languages}
Stars: {stars}
Topics: {topics}
License: {license}

Directory Structure:
{directory_structure}

Key Configuration Files:
{key_files}

README excerpt:
{readme_excerpt}

Respond with this exact JSON structure:
{{
    "project_name": "string",
    "description": "detailed 3-5 sentence description",
    "tech_stack": ["list", "of", "technologies"],
    "architecture_summary": "detailed 4-6 sentence architecture overview",
    "key_features": ["feature1", "feature2", "feature3", "feature4", "feature5"]
}}""")
        ])

        key_files_str = "\n".join(
            [f"\n--- {path} ---\n{content}"
             for path, content in repo_data.get("key_files", {}).items()]
        )

        languages = repo_data["metadata"].get("languages", {})
        languages_str = ", ".join(languages.keys()) if languages else repo_data["metadata"].get("language", "Unknown")

        chain = prompt | self.llm | StrOutputParser()

        result = await self._invoke_with_retry(chain, {
            "repo_url": repo_data.get("repo_url", ""),
            "name": repo_data["metadata"].get("name", ""),
            "description": repo_data["metadata"].get("description", "No description"),
            "language": repo_data["metadata"].get("language", "Unknown"),
            "languages": languages_str,
            "stars": repo_data["metadata"].get("stargazers_count", 0),
            "topics": ", ".join(repo_data["metadata"].get("topics", [])),
            "license": repo_data["metadata"].get("license", "Unknown"),
            "directory_structure": repo_data.get("directory_structure", ""),
            "key_files": key_files_str[:3000] if key_files_str else "None found",
            "readme_excerpt": repo_data.get("readme", "")[:4000],
        })

        try:
            cleaned = result.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                "project_name": repo_data["metadata"].get("name", "Unknown"),
                "description": repo_data["metadata"].get("description", "N/A"),
                "tech_stack": [repo_data["metadata"].get("language", "Unknown")],
                "architecture_summary": "Could not parse AI response for architecture.",
                "key_features": [],
            }

    async def generate_interview_questions(
        self,
        project_analysis: dict,
        repo_data: dict,
        difficulty: str = "intermediate",
        num_questions: int = 10,
    ) -> list:
        """Generate interview questions based on the project analysis."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior technical interviewer who creates thoughtful,
challenging interview questions about software projects. Generate questions that test
deep understanding of the project's architecture, design decisions, and technical details.
You MUST respond with valid JSON only. No markdown, no explanation outside JSON."""),
            ("human", """Generate {num_questions} interview questions about this project:

Project: {project_name}
Description: {description}
Tech Stack: {tech_stack}
Architecture: {architecture_summary}
Key Features: {key_features}
Difficulty Level: {difficulty}

Directory Structure:
{directory_structure}

README excerpt:
{readme_excerpt}

Respond with this exact JSON structure:
{{
    "questions": [
        {{
            "question": "the interview question",
            "category": "Conceptual|Technical|Architecture|Debugging|System Design",
            "difficulty": "{difficulty}",
            "hint": "a helpful hint for the candidate",
            "sample_answer": "a detailed sample answer (3-5 sentences)"
        }}
    ]
}}""")
        ])

        chain = prompt | self.llm | StrOutputParser()

        result = await self._invoke_with_retry(chain, {
            "num_questions": num_questions,
            "project_name": project_analysis.get("project_name", ""),
            "description": project_analysis.get("description", ""),
            "tech_stack": ", ".join(project_analysis.get("tech_stack", [])),
            "architecture_summary": project_analysis.get("architecture_summary", ""),
            "key_features": ", ".join(project_analysis.get("key_features", [])),
            "difficulty": difficulty,
            "directory_structure": repo_data.get("directory_structure", ""),
            "readme_excerpt": repo_data.get("readme", "")[:3000],
        })

        try:
            cleaned = result.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            parsed = json.loads(cleaned)
            return parsed.get("questions", [])
        except json.JSONDecodeError:
            return [
                {
                    "question": f"What is the primary purpose of {project_analysis.get('project_name', 'this project')}?",
                    "category": "Conceptual",
                    "difficulty": difficulty,
                    "hint": "Review the project description.",
                    "sample_answer": "Could not generate detailed questions due to parsing error.",
                }
            ]

    async def generate_setup_instructions(
        self,
        project_analysis: dict,
        repo_data: dict,
    ) -> dict:
        """Generate step-by-step setup instructions for the project."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a DevOps engineer and technical writer who creates clear,
step-by-step setup guides for software projects. Be specific with commands and include
warnings for common pitfalls. You MUST respond with valid JSON only. No markdown, no explanation outside JSON."""),
            ("human", """Generate setup instructions for this project:

Repository: {repo_url}
Project: {project_name}
Description: {description}
Language: {language}
Tech Stack: {tech_stack}
Default Branch: {default_branch}

Key Configuration Files:
{key_files}

Directory Structure:
{directory_structure}

README excerpt:
{readme_excerpt}

Respond with this exact JSON structure:
{{
    "prerequisites": ["prerequisite1", "prerequisite2", ...],
    "setup_steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "command": "exact terminal command or null",
            "description": "Detailed explanation of the step (2-3 sentences)",
            "warning": "warning or null"
        }}
    ],
    "potential_issues": [
        "Common issue 1 and how to fix it",
        "Common issue 2 and how to fix it"
    ]
}}""")
        ])

        key_files_str = "\n".join(
            [f"\n--- {path} ---\n{content}"
             for path, content in repo_data.get("key_files", {}).items()]
        )

        chain = prompt | self.llm | StrOutputParser()

        result = await self._invoke_with_retry(chain, {
            "repo_url": repo_data.get("repo_url", ""),
            "project_name": project_analysis.get("project_name", ""),
            "description": project_analysis.get("description", ""),
            "language": repo_data["metadata"].get("language", ""),
            "tech_stack": ", ".join(project_analysis.get("tech_stack", [])),
            "default_branch": repo_data["metadata"].get("default_branch", "main"),
            "key_files": key_files_str[:3000] if key_files_str else "None found",
            "directory_structure": repo_data.get("directory_structure", ""),
            "readme_excerpt": repo_data.get("readme", "")[:4000],
        })

        try:
            cleaned = result.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                "prerequisites": [],
                "setup_steps": [],
                "potential_issues": ["Could not parse setup instructions from AI response."],
            }
