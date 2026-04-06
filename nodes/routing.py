from graph_state import GraphState


def route_after_collect_input(state: GraphState) -> str:
    return "review_chapter" if state["mode"] == "template" else "collect_chapters"


def route_after_human_review(state: GraphState) -> str:
    return "approve_chapter" if state["action"] == "approve" else "refine_chapter"


def route_after_approve(state: GraphState) -> str:
    idx = state["current_chapter_index"]  # already incremented by approve_chapter
    if idx < len(state["chapters"]):
        return "generate_chapter"
    return "save_output"


def route_after_chapters_review(state: GraphState) -> str:
    return "generate_chapter" if state["action"] == "approve" else "update_chapter"