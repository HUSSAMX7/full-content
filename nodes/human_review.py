from langgraph.types import interrupt

from graph_state import GraphState
from nodes.classify_response import _classify_response


def human_review(state: GraphState) -> dict:
    idx = state["current_chapter_index"]
    total = len(state["chapters"])
    chapter_title = state["chapters"][idx]["title"]

    response = interrupt(
        f"--- Chapter {idx + 1}/{total}: {chapter_title} ---\n\n"
        f"{state['draft']}\n\n"
        "---\n"
        "Type your approval (e.g. good / perfect / ok) to move to the next chapter, "
        "or enter your revision notes:"
    )

    action = _classify_response(response)
    if action == "approve":
        return {"action": "approve"}
    if action == "regenerate":
        return {
            "action": "regenerate",
            "raw_feedback": response,
            "text_analysis": [],
            "feedback_notes": [],
        }
    return {"action": "refine", "raw_feedback": response}
