from typing import Annotated, TypedDict
import operator


class GraphState(TypedDict):
    references_content: str
    chapter_samples: str
    template: str
    general_project_context: str
    mode: str  # "template" or "manual" or "zero_data"
    topic: str
    doc_type: str # powerpoint or pdf
    requested_chapter_count: int # number of chapters to generate for zero-data mode
    chapters: list[dict]
    current_chapter_index: int
    draft: str
    feedback: Annotated[list[str], operator.add]
    action: str
    generated_chapters: Annotated[list[str], operator.add]

