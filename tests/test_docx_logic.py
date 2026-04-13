import os
import shutil
from tools.docx_builder import build_coach_script

def test_docx_generation():
    print("\n--- Testing DOCX Generation ---")
    
    # Mock content
    mock_content = {
        "lesson_title": "Understanding Torque",
        "opening_hook": "Have you ever tried to open a heavy door by pushing near the hinges?",
        "slides": [
            {
                "title": f"Torque Basics Slide {i+1}",
                "bullet_points": [f"Point {i+1}.1", f"Point {i+1}.2"],
                "example": f"Example for slide {i+1}"
            } for i in range(8)
        ],
        "closing_exercise": {
            "title": "The Human Wrench",
            "instructions": "Try pushing the door.",
            "expected_outcome": "Easier further away."
        },
        "coach_script": {
            "intro": "Welcome to the torque lesson.",
            "per_slide": [f"This is what you say for slide {i+1}." for i in range(8)],
            "wrap_up": "Great job today!"
        }
    }
    
    # Create temp output folder
    output_dir = "tmp_test_docx_output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        file_path = build_coach_script(mock_content, output_dir)
        
        assert os.path.exists(file_path)
        assert file_path.endswith(".docx")
        print(f"DOCX Generation: PASSED ({file_path})")
    finally:
        # Clean up
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

if __name__ == "__main__":
    test_docx_generation()
