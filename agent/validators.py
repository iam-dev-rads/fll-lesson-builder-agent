from pydantic import BaseModel, Field, field_validator, AliasChoices, model_validator
from typing import List, Optional

class SlideContent(BaseModel):
    """
    Validation model for individual slide content with defensive parser logic.
    """
    slide_number: int
    title: str = Field(..., max_length=60)
    bullet_points: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("bullet_points", "bullets", "bulletPoints")
    )
    example: str = Field(
        default="Think about how this applies to everyday life.", 
        validation_alias=AliasChoices("example", "real_world_example", "realWorldExample", "illustration")
    )
    speaker_note: str = Field(
        default="Let's discuss this concept as a team.", 
        validation_alias=AliasChoices("speaker_note", "speakerNote", "notes", "speaker_notes")
    )

    @model_validator(mode="before")
    @classmethod
    def clean_slide_content(cls, data: any) -> any:
        if not isinstance(data, dict):
            return data
        
        # 1. Clean title
        title = data.get("title")
        if isinstance(title, str):
            title = title.strip()
            if len(title) > 60:
                title = title[:57] + "..."
            data["title"] = title
            
        # 2. Clean bullet_points
        bps = data.get("bullet_points") or data.get("bullets") or data.get("bulletPoints")
        if bps:
            if isinstance(bps, str):
                bps = [bps]
            elif isinstance(bps, list):
                cleaned_bps = []
                for bp in bps:
                    bp_str = str(bp).strip()
                    if len(bp_str) > 120:
                        bp_str = bp_str[:117] + "..."
                    cleaned_bps.append(bp_str)
                # Limit to 4 bullet points, ensure at least 1
                bps = cleaned_bps[:4]
                if len(bps) < 1:
                    bps = ["Discuss this point with the team."]
            data["bullet_points"] = bps
        else:
            data["bullet_points"] = ["Discuss this point with the team."]

        # 3. Clean example
        example = data.get("example") or data.get("real_world_example") or data.get("realWorldExample") or data.get("illustration")
        if example:
            example_str = str(example).strip()
            if len(example_str) > 200:
                example_str = example_str[:197] + "..."
            data["example"] = example_str
        else:
            data["example"] = "Think about how this applies to everyday life."

        # 4. Clean speaker_note
        note = data.get("speaker_note") or data.get("speakerNote") or data.get("notes") or data.get("speaker_notes")
        if note:
            note_str = str(note).strip()
            if len(note_str) > 300:
                note_str = note_str[:297] + "..."
            data["speaker_note"] = note_str
        else:
            data["speaker_note"] = "Let's discuss this concept as a team."

        return data

class ClosingExercise(BaseModel):
    """
    Validation model for the final lesson activity.
    """
    title: str = Field(default="Closing Activity")
    instructions: str = Field(default="Work with your team to review what we learned.")
    expected_outcome: str = Field(default="Team understands the lesson concept.")

    @model_validator(mode="before")
    @classmethod
    def clean_closing_exercise(cls, data: any) -> any:
        if isinstance(data, str):
            return {
                "title": "Closing Exercise",
                "instructions": data,
                "expected_outcome": "Team understands the lesson concept."
            }
        return data

class CoachScript(BaseModel):
    """
    Validation model for the coach's instructional script.
    """
    intro: str = Field(default="Let's start our lesson.", validation_alias=AliasChoices("intro", "introduction", "opening"))
    per_slide: List[str] = Field(default_factory=list)
    wrap_up: str = Field(default="Great job today!", validation_alias=AliasChoices("wrap_up", "conclusion", "closing"))

    @model_validator(mode="before")
    @classmethod
    def clean_coach_script(cls, data: any) -> any:
        if isinstance(data, str):
            return {
                "intro": data,
                "per_slide": [],
                "wrap_up": "Great job today!"
            }
        return data

class LessonContent(BaseModel):
    """
    Root validation model for the complete lesson plan.
    """
    lesson_title: str
    grade_level: str = "5th-8th grade"
    slides: List[SlideContent]
    opening_hook: str = Field(default="Who can tell me something about today's topic?")
    closing_exercise: ClosingExercise
    coach_script: CoachScript

    @model_validator(mode="before")
    @classmethod
    def clean_lesson_content(cls, data: any) -> any:
        if not isinstance(data, dict):
            return data
        
        # Make sure closing_exercise is present
        if "closing_exercise" not in data or data["closing_exercise"] is None:
            data["closing_exercise"] = {
                "title": "Closing Exercise",
                "instructions": "Practice what we learned today.",
                "expected_outcome": "Better understanding."
            }
            
        # Make sure coach_script is present
        if "coach_script" not in data or data["coach_script"] is None:
            data["coach_script"] = {
                "intro": "Welcome, everyone!",
                "per_slide": [],
                "wrap_up": "Great job today!"
            }
            
        return data

    @field_validator("slides")
    @classmethod
    def validate_slides_count(cls, v: List[SlideContent]) -> List[SlideContent]:
        if len(v) < 5:
            raise ValueError("Lesson must have at least 5 slides")
        if len(v) > 10:
            return v[:10]
        return v
