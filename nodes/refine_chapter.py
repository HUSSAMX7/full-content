from langchain_core.messages import HumanMessage, SystemMessage

from graph_state import GraphState
from llm_config import llm


def refine_chapter(state: GraphState) -> dict:
    idx = state["current_chapter_index"]
    chapter = state["chapters"][idx]
    chapter_title = chapter["title"]
    chapter_description = chapter.get("description", "")
    topic = state["topic"]
    source_content = state["content"]
    latest_feedback = state["feedback"][-1]

    system_prompt = (
        "You are a specialist technical writer. Your task is to revise a chapter based on reviewer feedback.\n\n"
        "Strict rules:\n"
        "1) Apply the reviewer's feedback precisely.\n"
        "2) Preserve the same length — do not extend the chapter or add new sections.\n"
        "3) Content must remain about the new topic only, not the reference document.\n"
        "4) Write in the same language as the reference.\n\n"
        f"Reference document (for style only):\n{source_content}"
    )

    user_prompt = (
        f"New topic: {topic}\n"
        f"Chapter title: {chapter_title}\n"
    )
    if chapter_description:
        user_prompt += f"Chapter description: {chapter_description}\n"
    user_prompt += (
        f"\nCurrent draft:\n{state['draft']}\n\n"
        f"Reviewer feedback:\n{latest_feedback}\n\n"
        "Revise the chapter according to the feedback while preserving the same length and style."
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)
    draft = f"# {chapter_title}\n\n{response.content}"
    return {"draft": draft}
