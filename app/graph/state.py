from operator import add
from typing import Annotated, TypedDict, Dict, List, Any
from app.models.schemas import DifficultyLevel


class RepoAnalysisState(TypedDict, total=False):
    """State for the LangGraph repository analysis workflow."""

    # Input
    github_url: str
    difficulty: DifficultyLevel
    num_questions: int

    # Intermediate - Raw GitHub Data
    repo_data: Dict[str, Any]

    # Intermediate - AI Analysis
    project_analysis: Dict[str, Any]

    # Intermediate - Interview Questions
    interview_questions: List[Dict[str, Any]]

    # Intermediate - Setup Instructions
    setup_instructions: Dict[str, Any]

    # Final Output
    final_response: Dict[str, Any]

    # Error tracking
    errors: Annotated[List[str], add]
