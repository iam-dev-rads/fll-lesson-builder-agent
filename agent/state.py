from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    """
    Represents the state of the FLL Lesson Builder Agent.
    """
    concept: str
    cleaned_concept: str
    structured_content: Dict[str, Any]
    pptx_path: str
    docx_path: str
    output_folder: str
    retry_count: int
    status: str
    error: Optional[str]
