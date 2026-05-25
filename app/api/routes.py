from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse
from app.graph.workflow import get_compiled_graph

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="RepoPilot AI")


@router.post("/analyze")
async def analyze_repo(request: AnalyzeRequest):
    """
    Full analysis: Fetch repo, analyze project, generate interview questions,
    and provide step-by-step setup instructions.
    """
    try:
        graph = get_compiled_graph()

        initial_state = {
            "github_url": request.github_url,
            "difficulty": request.difficulty,
            "num_questions": request.num_questions,
            "errors": [],
        }

        result = await graph.ainvoke(initial_state)
        final_response = result.get("final_response", {})

        return final_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/questions-only")
async def generate_questions_only(request: AnalyzeRequest):
    """Generate only interview questions (faster endpoint)."""
    try:
        from app.core.github_client import GitHubClient
        from app.services.llm_service import LLMService

        github_client = GitHubClient()
        llm_service = LLMService()

        repo_data = await github_client.get_full_repo_data(request.github_url)
        analysis = await llm_service.analyze_project(repo_data)
        questions = await llm_service.generate_interview_questions(
            project_analysis=analysis,
            repo_data=repo_data,
            difficulty=request.difficulty,
            num_questions=request.num_questions,
        )

        return {
            "project_name": analysis.get("project_name", ""),
            "questions": questions,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/setup-only")
async def generate_setup_only(request: AnalyzeRequest):
    """Generate only setup instructions (faster endpoint)."""
    try:
        from app.core.github_client import GitHubClient
        from app.services.llm_service import LLMService

        github_client = GitHubClient()
        llm_service = LLMService()

        repo_data = await github_client.get_full_repo_data(request.github_url)
        analysis = await llm_service.analyze_project(repo_data)
        setup = await llm_service.generate_setup_instructions(
            project_analysis=analysis,
            repo_data=repo_data,
        )

        return {
            "project_name": analysis.get("project_name", ""),
            "setup": setup,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
