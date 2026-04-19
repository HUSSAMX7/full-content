from langgraph.types import interrupt

from graph_state import GraphState
from llm_config import llm
from schemas import ChapterList

_structured_llm = llm.with_structured_output(ChapterList)


def collect_chapters(state: GraphState) -> dict:
    topic = state["topic"]

    response = interrupt(
        f"Topic: {topic}\n\n"
        "What chapters do you want? (any format: numbered, comma-separated, or free text)\n"
    )

    from langchain_core.messages import HumanMessage, SystemMessage
    messages = [
        SystemMessage(
            content=(
                "Extract chapter titles from the user's input.\n"
                "Rules:\n"
                "1) Each numbered item or line is a separate chapter.\n"
                "2) Infer the chapter title from the main subject of the line — do not copy the full line as the title.\n"
                "3) Any extra detail or explanation in the same line becomes the description.\n"
                "4) Never merge multiple lines into one chapter.\n"
                "5) If no description exists, leave it empty."
            )
        ),
        HumanMessage(content=f"Topic: {topic}\nUser input:\n{response}"),
    ]
    result = _structured_llm.invoke(messages)
    chapters = [{"title": c.title, "description": c.description} for c in result.chapters]
    return {"chapters": chapters}
