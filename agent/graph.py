import logging
from typing import Dict, Any, Literal

from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    validate_input_node,
    generate_content_node,
    validate_content_node,
    create_output_folder_node,
    error_node
)
from tools.pptx_builder import build_presentation
from tools.docx_builder import build_coach_script

# Configure logging
logger = logging.getLogger(__name__)

async def build_pptx_node(state: AgentState) -> Dict[str, Any]:
    """
    Inline node to build the PowerPoint presentation using tools.
    """
    logger.info("Building PowerPoint presentation...")
    path = build_presentation(
        state["structured_content"],
        state["output_folder"]
    )
    return {
        "pptx_path": path,
        "status": "pptx_created"
    }

async def build_docx_node(state: AgentState) -> Dict[str, Any]:
    """
    Inline node to build the Word document coach script using tools.
    """
    logger.info("Building Word coach script...")
    path = build_coach_script(
        state["structured_content"],
        state["output_folder"]
    )
    return {
        "docx_path": path,
        "status": "docx_created"
    }

def content_router(state: AgentState) -> Literal["retry", "error", "continue"]:
    """
    Determines whether to retry content generation, fail, or proceed based on validation errors.
    """
    error = state.get("error")
    retry_count = state.get("retry_count", 0)
    
    if error and retry_count < 3:
        logger.warning(f"Validation error encountered. Retrying ({retry_count}/3)... Error: {error}")
        return "retry"
    elif error:
        logger.error(f"Execution halted. Problem: {error}")
        return "error"
    else:
        return "continue"

# 1. Define the Graph
workflow = StateGraph(AgentState)

# 2. Add all nodes to the workfow
workflow.add_node("validate_input", validate_input_node)
workflow.add_node("generate_content", generate_content_node)
workflow.add_node("validate_content", validate_content_node)
workflow.add_node("create_output_folder", create_output_folder_node)
workflow.add_node("build_pptx", build_pptx_node)
workflow.add_node("build_docx", build_docx_node)
workflow.add_node("error", error_node)

# 3. Define the edges between nodes
workflow.set_entry_point("validate_input")

workflow.add_edge("validate_input", "generate_content")
workflow.add_edge("generate_content", "validate_content")

workflow.add_conditional_edges(
    "validate_content",
    content_router,
    {
        "retry": "generate_content",
        "error": "error",
        "continue": "create_output_folder"
    }
)

workflow.add_edge("create_output_folder", "build_pptx")
workflow.add_edge("build_pptx", "build_docx")
workflow.add_edge("build_docx", END)
workflow.add_edge("error", END)

# 4. Compile the graph
lesson_graph = workflow.compile()

async def run_pipeline(concept: str) -> Dict[str, Any]:
    """
    Top-level helper function to run the entire FLL Lesson Builder pipeline.
    """
    logger.info(f"--- Starting FLL Lesson Builder Pipeline for: {concept} ---")
    
    initial_state = {
        "concept": concept,
        "retry_count": 0,
        "status": "started",
        "error": None
    }
    
    try:
        final_state = await lesson_graph.ainvoke(initial_state)
        logger.info(f"--- Pipeline Completed | Status: {final_state.get('status')} ---")
        return final_state
    except Exception as e:
        logger.exception(f"Pipeline crash: {str(e)}")
        return {
            "status": "crashed",
            "error": str(e)
        }
