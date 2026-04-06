from langchain_core.messages import HumanMessage, SystemMessage

from graph_state import GraphState
from llm_config import llm


def generate_chapter(state: GraphState) -> dict:
    idx = state["current_chapter_index"]
    chapter = state["chapters"][idx]
    chapter_title = chapter["title"]
    chapter_description = chapter.get("description", "")
    topic = state["topic"]
    source_content = state["content"]

    system_prompt = (
        "You are a specialist technical writer. Your task is to write one specific chapter "
        "about a new topic, following the style of the reference document.\n\n"
        "Strict rules:\n"
        "1) Write only the requested chapter — do not write content from other chapters.\n"
        "2) Length: approximately the same length as the equivalent chapter in the reference.\n"
        "3) Do not add subheadings or bullet lists unless they are used in the reference for the same chapter type.\n"
        "4) The reference document = a model for style and length only. Do not copy its content.\n"
        "5) Write about the new topic only, in the same language as the reference.\n"
        "6) Never mention the reference project.\n\n"
        f"Reference document (for style and length only):\n{source_content}"
    )

    user_prompt = (
        f"New topic: {topic}\n"
        f"Chapter title: {chapter_title}\n"
    )
    if chapter_description:
        user_prompt += f"Chapter description: {chapter_description}\n"
    user_prompt += (
        f"\nWrite only the content of the '{chapter_title}' chapter, matching the size and style "
        "of the equivalent chapter in the reference. Do not write the full document — this chapter only."
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)
    draft = f"# {chapter_title}\n\n{response.content}"
    return {"draft": draft}
