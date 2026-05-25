from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class AnalyzeRequest(BaseModel):
    github_url: str = Field(
        ...,
        description="GitHub repository URL",
        examples=["https://github.com/langchain-ai/langchain"]
    )
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE,
        description="Difficulty level for interview questions"
    )
    num_questions: int = Field(
        default=10,
        ge=3,
        le=25,
        description="Number of interview questions to generate"
    )


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str
    hint: Optional[str] = None
    sample_answer: str


class SetupStep(BaseModel):
    step_number: int
    title: str
    command: Optional[str] = None
    description: str
    warning: Optional[str] = None


class ProjectAnalysis(BaseModel):
    project_name: str
    description: str
    tech_stack: List[str]
    architecture_summary: str
    key_features: List[str]


class AnalyzeResponse(BaseModel):
    project_analysis: ProjectAnalysis
    interview_questions: List[InterviewQuestion]
    setup_instructions: List[SetupStep]
    prerequisites: List[str]
    potential_issues: List[str]


class HealthResponse(BaseModel):
    status: str
    service: str
