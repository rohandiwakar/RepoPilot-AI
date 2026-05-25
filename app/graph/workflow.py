from langgraph.graph import StateGraph, END
from app.graph.state import RepoAnalysisState
from app.graph.nodes import (
    fetch_repo_data,
    analyze_project,
    generate_questions,
    generate_setup,
    compile_response,
)


def should_continue_after_fetch(state: RepoAnalysisState) -> str:
    """Conditional edge: if fetch failed, go to compile; otherwise analyze."""
    if not state.get("repo_data"):
        return "compile"
    return "analyze"


def build_analysis_graph() -> StateGraph:
    """Build the LangGraph workflow for repository analysis."""

    # Create the graph
    workflow = StateGraph(RepoAnalysisState)

    # Add nodes
    workflow.add_node("fetch_repo", fetch_repo_data)
    workflow.add_node("analyze", analyze_project)
    workflow.add_node("generate_questions", generate_questions)
    workflow.add_node("generate_setup", generate_setup)
    workflow.add_node("compile", compile_response)

    # Set entry point
    workflow.set_entry_point("fetch_repo")

    # Add conditional edge after fetch
    workflow.add_conditional_edges(
        "fetch_repo",
        should_continue_after_fetch,
        {
            "analyze": "analyze",
            "compile": "compile",
        }
    )

    # After analysis, fan out to questions AND setup (parallel)
    workflow.add_edge("analyze", "generate_questions")
    workflow.add_edge("analyze", "generate_setup")

    # Both converge to compile
    workflow.add_edge("generate_questions", "compile")
    workflow.add_edge("generate_setup", "compile")

    # End after compile
    workflow.add_edge("compile", END)

    return workflow


def get_compiled_graph():
    """Compile and return the executable graph."""
    workflow = build_analysis_graph()
    return workflow.compile()
