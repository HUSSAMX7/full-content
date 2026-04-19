from typing import Annotated, TypedDict
import operator


class GraphState(TypedDict):
    references_content: str
    chapter_samples: str
    template: str
    general_project_context: str
    mode: str
    topic: str
    doc_type: str
    requested_chapter_count: int
    chapters: list[dict]
    current_chapter_index: int
    draft: str
    raw_feedback: str
    text_analysis: list[str]
    feedback_notes: list[str]
    action: str
    regeneration_notes: list[str]
    generated_chapters: Annotated[list[str], operator.add]