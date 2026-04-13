import asyncio
import os
import shutil
from agent.nodes import validate_input_node, validate_content_node, create_output_folder_node
from agent.state import AgentState

async def test_input_validation():
    print("\n--- Testing Input Validation ---")
    state = {"concept": "gear ratios"}
    result = await validate_input_node(state)
    assert result["cleaned_concept"] == "Gear ratios"
    assert result["status"] == "input_validated"
    print("Input Validation: PASSED")

async def test_folder_creation():
    print("\n--- Testing Folder Creation ---")
    state = {"cleaned_concept": "Gear ratios"}
    result = await create_output_folder_node(state)
    folder = result["output_folder"]
    assert "gear_ratios" in folder
    assert os.path.exists(folder)
    print(f"Folder Creation: PASSED ({folder})")
    # Clean up
    # shutil.rmtree(folder) # Keep it for manual check if needed

async def test_content_validation():
    print("\n--- Testing Content Validation ---")
    raw_json = """
    Sure, here is your lesson:
    {
      "lesson_title": "Gears 101",
      "grade_level": "5th-8th grade",
      "slides": [
        {"slide_number": 1, "title": "Intro", "bullet_points": ["A", "B"], "example": "Bike", "speaker_note": "Hi"}
      ] * 8,
      "opening_hook": "Hook",
      "closing_exercise": {"title": "T", "instructions": "I", "expected_outcome": "O"},
      "coach_script": {"intro": "Hi", "per_slide": ["S"] * 8, "wrap_up": "Bye"}
    }
    """
    # Fix the Python-style list multiplication in the mock string for actual JSON
    slide = '{"slide_number": 1, "title": "Intro", "bullet_points": ["A", "B"], "example": "Bike", "speaker_note": "Hi"}'
    slides = ",".join([slide] * 8)
    script_items = ",".join(['"S"'] * 8)
    
    clean_json = f"""
    {{
      "lesson_title": "Gears 101",
      "grade_level": "5th-8th grade",
      "slides": [{slides}],
      "opening_hook": "Hook",
      "closing_exercise": {{"title": "T", "instructions": "I", "expected_outcome": "O"}},
      "coach_script": {{"intro": "Hi", "per_slide": [{script_items}], "wrap_up": "Bye"}}
    }}
    """
    state = {"structured_content": f"Some text before {clean_json} and after."}
    result = await validate_content_node(state)
    assert result["status"] == "content_validated"
    assert isinstance(result["structured_content"], dict)
    print("Content Validation: PASSED")

async def run_tests():
    await test_input_validation()
    await test_folder_creation()
    await test_content_validation()

if __name__ == "__main__":
    asyncio.run(run_tests())
