from agent.validators import LessonContent, SlideContent, ClosingExercise, CoachScript
import pytest
from pydantic import ValidationError

def test_valid_lesson():
    slide = {
        "slide_number": 1,
        "title": "Introduction to Robotics",
        "bullet_points": ["Point 1", "Point 2"],
        "example": "Lego Spike Prime",
        "speaker_note": "Welcome the class."
    }
    data = {
        "lesson_title": "FLL Basics",
        "grade_level": "5th-8th grade",
        "slides": [slide] * 8,
        "opening_hook": "Imagine a world fixed by robots.",
        "closing_exercise": {
            "title": "Build a base",
            "instructions": "Use 4 beams.",
            "expected_outcome": "A stable base."
        },
        "coach_script": {
            "intro": "Hi team",
            "per_slide": ["Intro"] * 8,
            "wrap_up": "Great job"
        }
    }
    lesson = LessonContent(**data)
    assert len(lesson.slides) == 8
    print("Test Valid Lesson: PASSED")

def test_too_few_slides():
    slide = {
        "slide_number": 1,
        "title": "Short",
        "bullet_points": ["A", "B"],
        "example": "ex",
        "speaker_note": "note"
    }
    data = {
        "lesson_title": "Too Short",
        "slides": [slide] * 4,
        "opening_hook": "hook",
        "closing_exercise": {
            "title": "t",
            "instructions": "i",
            "expected_outcome": "o"
        },
        "coach_script": {
            "intro": "i",
            "per_slide": ["p"] * 4,
            "wrap_up": "w"
        }
    }
    try:
        LessonContent(**data)
    except ValidationError as e:
        assert "Lesson must have at least 5 slides" in str(e)
        print("Test Too Few Slides: PASSED")

def test_trim_slides():
    slide = {
        "slide_number": 1,
        "title": "Many",
        "bullet_points": ["A", "B"],
        "example": "ex",
        "speaker_note": "note"
    }
    data = {
        "lesson_title": "Too Many",
        "slides": [slide] * 12,
        "opening_hook": "hook",
        "closing_exercise": {
            "title": "t",
            "instructions": "i",
            "expected_outcome": "o"
        },
        "coach_script": {
            "intro": "i",
            "per_slide": ["p"] * 12,
            "wrap_up": "w"
        }
    }
    lesson = LessonContent(**data)
    assert len(lesson.slides) == 10
    print("Test Trim Slides: PASSED")

def test_aliases():
    print("\n--- Testing Pydantic Aliases ---")
    slide = {
        "slide_number": 1,
        "title": "Alias Test",
        "bullets": ["Point 1", "Point 2"], # Alias for bullet_points
        "example": "Ex",
        "notes": "Speaker notes" # Alias for speaker_note
    }
    data = {
        "lesson_title": "Alias Test",
        "grade_level": "5th-8th grade",
        "slides": [slide] * 8,
        "opening_hook": "Hook",
        "closing_exercise": {
            "title": "T",
            "instructions": "I",
            "expected_outcome": "O"
        },
        "coach_script": {
            "introduction": "Welcome", # Alias for intro
            "per_slide": ["Intro"] * 8,
            "conclusion": "Bye" # Alias for wrap_up
        }
    }
    lesson = LessonContent(**data)
    assert lesson.coach_script.intro == "Welcome"
    assert lesson.coach_script.wrap_up == "Bye"
    assert lesson.slides[0].bullet_points == ["Point 1", "Point 2"]
    assert lesson.slides[0].speaker_note == "Speaker notes"
    print("Test Aliases: PASSED")

if __name__ == "__main__":
    test_valid_lesson()
    test_too_few_slides()
    test_trim_slides()
    test_aliases()
