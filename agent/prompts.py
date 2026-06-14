def build_lesson_prompt(concept: str) -> str:
    """
    Builds the initial lesson generation prompt for the LLM.
    """
    prompt = f"""
You are an expert FLL (FIRST LEGO League) robotics coach. 
Your goal is to create a complete lesson plan to teach the concept of "{concept}" to a team of girls aged 9-14.

### INSTRUCTIONS:
1. TARGET AUDIENCE: Girls aged 9-14. Use an encouraging, empowering, and fun tone.
2. LANGUAGE: Use simple English. Explain concepts as if you are talking to a 5th grader.
3. JARGON: Never use a technical term (like "PID loop", "torque", or "variable") without explaining it in simple terms first.
4. EXAMPLES: Use real-world, relatable examples that a 10-year-old would know (e.g., sports, music, cooking, games, everyday life).
5. STRUCTURE:
   - Decide between 5 to 10 slides based on the complexity of "{concept}". (Simple concept = 5 slides, complex = 8 to 10 slides).
   - Every slide must include a relatable real-world example.
   - The lesson must include an "opening hook" (a fun question or story).
   - The lesson must include a "closing exercise" that kids can do in the room in under 10 minutes.
6. FORMAT: Return ONLY a valid JSON object. No markdown, no preamble, no explanations. Just the JSON.

### JSON SCHEMA:
{{
  "lesson_title": "A fun and catchy title",
  "grade_level": "5th-8th grade",
  "slides": [
    {{
      "slide_number": 1,
      "title": "Title of the slide",
      "bullet_points": ["2 to 4 bullet points only", "Each bullet must be under 120 chars"],
      "example": "A real-world example related to this specific slide (REQUIRED)",
      "speaker_note": "What the coach should say out loud (max 300 chars)"
    }}
  ],
  "opening_hook": "A fun question or story to grab their attention",
  "closing_exercise": {{
    "title": "Hands-on activity name",
    "instructions": "Simple step-by-step instructions",
    "expected_outcome": "What the kids should learn or see"
  }},
  "coach_script": {{
    "intro": "What the coach says to start the lesson",
    "per_slide": ["One instructional sentence per slide, matching the slide count"],
    "wrap_up": "Empowering closing statement"
  }}
}}

### CRITICAL FORMATTING RULES:
- "closing_exercise" MUST be a JSON object with keys: title, instructions, expected_outcome. Do NOT return it as a string.
- "coach_script" MUST be a JSON object with keys: intro, per_slide, wrap_up. Do NOT return it as a string.
- "coach_script.per_slide" MUST be a list of plain strings. Do NOT return a list of objects or dictionaries.
- Ensure every slide in the "slides" list has "bullet_points", "example" (which is REQUIRED), and "speaker_note" fields.

### EXAMPLE STRUCTURE (FOLLOW THIS):
{{
  "lesson_title": "The Power of Gears",
  "grade_level": "5th-8th grade",
  "slides": [
    {{
      "slide_number": 1,
      "title": "What are Gears?",
      "bullet_points": ["Gears are wheels with teeth.", "They help move things."],
      "example": "The chain and gears on your bicycle.",
      "speaker_note": "Hi team! Ever wonder how your bike moves so fast?"
    }}
  ],
  "opening_hook": "Who here has ridden a bike with 21 gears?",
  "closing_exercise": {{
    "title": "Gear Mesh",
    "instructions": "Connect two gears and spin them.",
    "expected_outcome": "You see how one moves the other."
  }},
  "coach_script": {{
    "intro": "Welcome back! Today we tackle gears.",
    "per_slide": ["Introduction to gear teeth."],
    "wrap_up": "You are all gear experts now!"
  }}
}}

Begin!
""".strip()
    return prompt

def build_retry_prompt(concept: str, error: str) -> str:
    """
    Builds a retry prompt when the previous LLM output was invalid.
    """
    prompt = f"""
I previously asked you to generate a lesson plan for "{concept}" in JSON format, but the result was invalid or did not follow the schema correctly.

ERROR ENCOUNTERED:
{error}

IMPORTANT: 
- You MUST return ONLY a valid JSON object. 
- Do not include markdown code blocks (```json).
- Do not include any introduction or closing text.
- Ensure the "slides" count matches the "per_slide" count in the script.
- Double-check your commas and brackets for valid JSON syntax.

Please try again and return ONLY the corrected JSON object.
""".strip()
    return prompt
