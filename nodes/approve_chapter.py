from graph_state import GraphState


def approve_chapter(state: GraphState) -> dict:
    return {
        "generated_chapters": [state["draft"]],
        "current_chapter_index": state["current_chapter_index"] + 1,
    }
