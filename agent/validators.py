from pydantic import BaseModel, Field, field_validator, AliasChoices
from typing import List, Optional

class SlideContent(BaseModel):
    """
    Validation model for individual slide content.
    """
    slide_number: int
    title: str = Field(..., max_length=60)
    bullet_points: List[str] = Field(
        ..., 
        min_length=2, 
        max_length=4, 
        validation_alias=AliasChoices("bullet_points", "bullets", "bulletPoints")
    )
    example: str = Field(..., max_length=200)
    speaker_note: str = Field(
        ..., 
        max_length=300, 
        validation_alias=AliasChoices("speaker_note", "speakerNote", "notes")
    )

    @field_validator("bullet_points")
    @classmethod
    def validate_bullet_length(cls, v: List[str]) -> List[str]:
        for bp in v:
            if len(bp) > 120:
                raise ValueError("Each bullet point must be max 120 characters")
        return v

class ClosingExercise(BaseModel):
    """
    Validation model for the final lesson activity.
    """
    title: str
    instructions: str
    expected_outcome: str

class CoachScript(BaseModel):
    """
    Validation model for the coach's instructional script.
    """
    intro: str = Field(..., validation_alias=AliasChoices("intro", "introduction", "opening"))
    per_slide: List[str]
    wrap_up: str = Field(..., validation_alias=AliasChoices("wrap_up", "conclusion", "closing"))

class LessonContent(BaseModel):
    """
    Root validation model for the complete lesson plan.
    """
    lesson_title: str
    grade_level: str = "5th-8th grade"
    slides: List[SlideContent]
    opening_hook: str
    closing_exercise: ClosingExercise
    coach_script: CoachScript

    @field_validator("slides")
    @classmethod
    def validate_slides_count(cls, v: List[SlideContent]) -> List[SlideContent]:
        if len(v) < 8:
            raise ValueError("Lesson must have at least 8 slides")
        if len(v) > 10:
            return v[:10]
        return v
