from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import interrupt

from graph_state import GraphState
from llm_config import llm
from schemas import ChapterList

_structured_llm = llm.with_structured_output(ChapterList)


def _parse_chapters(template_text: str) -> list[dict]:
    messages = [
        SystemMessage(
            content=(
                "Extract chapter titles and their descriptions from the template.\n"
                "Descriptions are written in brackets [] after each title.\n"
                "If no description exists, leave it empty."
            )
        ),
        HumanMessage(content=f"Template content:\n{template_text}"),
    ]
    result = _structured_llm.invoke(messages)
    return [{"title": c.title, "description": c.description} for c in result.chapters]


def _extract_topic(template_text: str) -> str:
    messages = [
        SystemMessage(content="Extract the main topic from this template in one short sentence."),
        HumanMessage(content=template_text),
    ]
    result = llm.invoke(messages)
    return result.content.strip()


def collect_input(state: GraphState) -> dict:
    mode = state["mode"]

    if mode == "template":
        template_text = state["template"]
        chapters = _parse_chapters(template_text)
        topic = _extract_topic(template_text)
        return {
            "topic": topic,
            "chapters": chapters,
            "current_chapter_index": 0,
        }

    # manual mode: ask for topic only, chapters collected in next node
    response = interrupt("Hello! What is the topic of your document?\n")
    return {
        "topic": response.strip(),
        "chapters": [],
        "current_chapter_index": 0,
    }
