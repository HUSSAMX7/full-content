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
                "Each chapter has a title and an optional description in brackets [].\n"
                "If no description exists, leave it empty."
            )
        ),
        HumanMessage(content=f"Topic: {topic}\nUser input:\n{response}"),
    ]
    result = _structured_llm.invoke(messages)
    chapters = [{"title": c.title, "description": c.description} for c in result.chapters]
    return {"chapters": chapters}
