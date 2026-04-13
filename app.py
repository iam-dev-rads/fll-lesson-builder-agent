import gradio as gr
import logging
import os
import asyncio
from agent.graph import run_pipeline

# Configure logging at the top of the file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_lesson(concept):
    """
    Async handler for the lesson generation process.
    Uses yielding to provide multi-step status updates directly to the Gradio UI.
    """
    # 1. Immediate Input Validation
    clean_concept = concept.strip() if concept else ""
    if not clean_concept or len(clean_concept) < 3:
        yield ("⚠️ Please enter a valid concept (at least 3 characters)", "", "", {})
        return

    # 2. Status Update: Beginning Process
    yield ("⏳ Generating lesson content... Calling Claude and building assets.", "", "", {})

    try:
        # 3. Invoke the LangGraph Pipeline
        # run_pipeline is already async and handles internal retries/errors
        result = await run_pipeline(clean_concept)

        # 4. Handle Pipeline Completion States
        status = result.get("status")
        
        if status == "failed":
            error_reason = result.get("error", "Process failed during one of the nodes.")
            yield (f"❌ Failed: {error_reason}", "", "", {})
            return
            
        if status == "crashed":
            error_msg = result.get("error", "Critical system error.")
            yield (f"💥 Pipeline crashed: {error_msg}", "", "", {})
            return

        # 5. Final Success Update
        yield (
            "✅ Lesson created successfully!",
            # Returns absolute paths for the user to find the files
            result.get("pptx_path", "Not generated"),
            result.get("docx_path", "Not generated"),
            # Shows the validated JSON for a quick curriculum check
            result.get("structured_content", {})
        )

    except Exception as e:
        logger.exception("Unexpected error in Gradio handler")
        yield (f"❌ Unexpected error: {str(e)}", "", "", {})

# Define UI Layout using gr.Blocks for a clean, professional feel
with gr.Blocks(title="FLL Lesson Builder", theme=gr.themes.Soft()) as demo:
    # Header Section
    gr.Markdown("# 🤖 FLL Lesson Builder")
    gr.Markdown("### AI-powered lesson generator for FLL coaches")
    
    # Input Section
    with gr.Row():
        concept_input = gr.Textbox(
            label="Enter the concept to teach",
            placeholder="e.g. Gear Ratios, Line Following, Engineering Design Process",
            lines=2,
            elem_id="concept_input"
        )
    
    # Action Button
    with gr.Row():
        generate_btn = gr.Button("Generate Lesson", variant="primary", scale=2)
        
    # Status Feedback
    with gr.Row():
        status_output = gr.Textbox(label="Status", interactive=False, placeholder="Waiting for input...")
        
    # File Path Outputs
    with gr.Row():
        pptx_output = gr.Textbox(label="PowerPoint saved to", interactive=False)
        docx_output = gr.Textbox(label="Coach Script saved to", interactive=False)
        
    # Data Inspection Preview
    with gr.Row():
        json_preview = gr.JSON(label="Lesson Content Preview")
        
    # Connect the handler
    # Note: Gradio handles async functions automatically
    generate_btn.click(
        fn=generate_lesson,
        inputs=[concept_input],
        outputs=[status_output, pptx_output, docx_output, json_preview]
    )

# Execution Entry Point
if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )
