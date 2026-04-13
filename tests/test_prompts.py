from agent.prompts import build_lesson_prompt, build_retry_prompt

def verify_prompts():
    concept = "Gear Ratios"
    error = "Missing comma on line 12"
    
    lesson_prompt = build_lesson_prompt(concept)
    retry_prompt = build_retry_prompt(concept, error)
    
    print("--- LESSON PROMPT ---")
    print(lesson_prompt)
    print("\n--- RETRY PROMPT ---")
    print(retry_prompt)
    
    # Simple checks
    assert concept in lesson_prompt
    assert "9-14" in lesson_prompt
    assert "JSON" in lesson_prompt
    assert error in retry_prompt
    print("\nPrompt Verification: PASSED")

if __name__ == "__main__":
    verify_prompts()
