from langchain_core.messages import HumanMessage, SystemMessage

from graph_state import GraphState
from llm_config import llm
from schemas import ChapterList

_structured_llm = llm.with_structured_output(ChapterList)


def propose_default_chapters(state: GraphState) -> dict:
    topic = state["topic"]
    doc_type = state["doc_type"]
    chapter_count = state["requested_chapter_count"]

    messages = [
        SystemMessage(
            content=(
                "You create a practical chapter outline.\n"
                "Return exactly the requested number of chapters.\n"
                "Each chapter must have: title + short description.\n"
                "Titles should be specific, ordered logically, and non-duplicated."
                )
        ),
        HumanMessage(content=f"Topic: {topic}\n"
        f"Document type: {doc_type}\n"
        f"Requested chapter count: {chapter_count}"),
    ]
    result = _structured_llm.invoke(messages)
    chapters = [{"title": c.title, "description": c.description} for c in result.chapters]
    return {"chapters": chapters}