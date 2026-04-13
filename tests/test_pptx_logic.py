import os
import shutil
from tools.pptx_builder import build_presentation

def test_pptx_generation():
    print("\n--- Testing PPTX Generation ---")
    
    # Mock content
    mock_content = {
        "lesson_title": "Understanding Torque",
        "opening_hook": "Have you ever tried to open a heavy door by pushing near the hinges?",
        "slides": [
            {
                "title": f"Torque Basics Slide {i+1}",
                "bullet_points": [f"Bullet point A for slide {i+1}", f"Bullet point B for slide {i+1}"],
                "example": f"This is a real-world example for slide {i+1} involving a wrench."
            } for i in range(8)
        ],
        "closing_exercise": {
            "title": "The Human Wrench",
            "instructions": "Try to push a door open from different distances from the hinge.",
            "expected_outcome": "You'll feel it is much easier to push when you are far from the hinge!"
        }
    }
    
    # Create temp output folder
    output_dir = "tmp_test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        file_path = build_presentation(mock_content, output_dir)
        
        assert os.path.exists(file_path)
        assert file_path.endswith(".pptx")
        print(f"PPTX Generation: PASSED ({file_path})")
    finally:
        # Clean up
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

if __name__ == "__main__":
    test_pptx_generation()
