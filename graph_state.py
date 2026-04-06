from typing import Annotated, TypedDict
import operator


class GraphState(TypedDict):
    content: str
    template: str
    mode: str  # "template" or "manual"
    topic: str
    chapters: list[dict]
    current_chapter_index: int
    draft: str
    feedback: Annotated[list[str], operator.add]
    action: str
    generated_chapters: Annotated[list[str], operator.add]

