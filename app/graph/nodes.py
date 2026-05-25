from app.graph.state import RepoAnalysisState
from app.core.github_client import GitHubClient
from app.services.llm_service import LLMService


async def fetch_repo_data(state: RepoAnalysisState) -> dict:
    """Node 1: Fetch repository data from GitHub API."""
    print("Node 1: Fetching repository data from GitHub...")

    github_url = state.get("github_url", "")
    try:
        github_client = GitHubClient()
        repo_data = await github_client.get_full_repo_data(github_url)
        print(f"Successfully fetched data for: {repo_data['metadata'].get('full_name', github_url)}")
        return {"repo_data": repo_data}
    except Exception as e:
        error_msg = f"Failed to fetch repo data: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "repo_data": {},
            "errors": [error_msg],
        }


async def analyze_project(state: RepoAnalysisState) -> dict:
    """Node 2: Analyze the project using Gemini LLM."""
    print("Node 2: Analyzing project with AI...")

    repo_data = state.get("repo_data", {})
    if not repo_data:
        error_msg = "No repo data available for analysis"
        print(f"Error: {error_msg}")
        return {
            "project_analysis": {},
            "errors": [error_msg],
        }

    try:
        llm_service = LLMService()
        project_analysis = await llm_service.analyze_project(repo_data)
        print(f"Analysis complete for: {project_analysis.get('project_name', 'Unknown')}")
        return {"project_analysis": project_analysis}
    except Exception as e:
        error_msg = f"Project analysis failed: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "project_analysis": {
                "project_name": repo_data["metadata"].get("name", "Unknown"),
                "description": repo_data["metadata"].get("description", "N/A"),
                "tech_stack": [repo_data["metadata"].get("language", "Unknown")],
                "architecture_summary": "Analysis failed.",
                "key_features": [],
            },
            "errors": [error_msg],
        }


async def generate_questions(state: RepoAnalysisState) -> dict:
    """Node 3: Generate interview questions based on the project analysis."""
    print("Node 3: Generating interview questions...")

    try:
        project_analysis = state.get("project_analysis", {})
        repo_data = state.get("repo_data", {})
        difficulty = state.get("difficulty", "intermediate")
        num_questions = state.get("num_questions", 10)

        llm_service = LLMService()
        questions = await llm_service.generate_interview_questions(
            project_analysis=project_analysis,
            repo_data=repo_data,
            difficulty=difficulty,
            num_questions=num_questions,
        )
        print(f"Generated {len(questions)} interview questions")
        return {"interview_questions": questions}
    except Exception as e:
        print(f"Error generating questions: {e}")
        return {
            "interview_questions": [],
            "errors": [f"Question generation failed: {str(e)}"],
        }


async def generate_setup(state: RepoAnalysisState) -> dict:
    """Node 4: Generate step-by-step setup instructions."""
    print("Node 4: Generating setup instructions...")

    try:
        project_analysis = state.get("project_analysis", {})
        repo_data = state.get("repo_data", {})

        llm_service = LLMService()
        setup = await llm_service.generate_setup_instructions(
            project_analysis=project_analysis,
            repo_data=repo_data,
        )
        print(f"Generated {len(setup.get('setup_steps', []))} setup steps")
        return {"setup_instructions": setup}
    except Exception as e:
        print(f"Error generating setup: {e}")
        return {
            "setup_instructions": {
                "prerequisites": [],
                "setup_steps": [],
                "potential_issues": [f"Setup generation failed: {str(e)}"],
            },
            "errors": [f"Setup generation failed: {str(e)}"],
        }


async def compile_response(state: RepoAnalysisState) -> dict:
    """Node 5: Compile the final response."""
    print("Node 5: Compiling final response...")

    project_analysis = state.get("project_analysis", {})
    questions = state.get("interview_questions", [])
    setup = state.get("setup_instructions", {})
    errors = state.get("errors", [])

    final_response = {
        "project_analysis": {
            "project_name": project_analysis.get("project_name", "Unknown"),
            "description": project_analysis.get("description", "N/A"),
            "tech_stack": project_analysis.get("tech_stack", []),
            "architecture_summary": project_analysis.get("architecture_summary", "N/A"),
            "key_features": project_analysis.get("key_features", []),
        },
        "interview_questions": questions,
        "setup_instructions": setup.get("setup_steps", []),
        "prerequisites": setup.get("prerequisites", []),
        "potential_issues": setup.get("potential_issues", []),
        "errors_encountered": errors,
    }

    print("Response compiled successfully!")
    return {"final_response": final_response}
