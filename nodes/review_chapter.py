from langgraph.types import interrupt

from graph_state import GraphState
from nodes.classify_response import _classify_response


def review_chapter(state: GraphState) -> dict:
    chapters = state["chapters"]

    lines = []
    for i, ch in enumerate(chapters):
        line = f"{i+1}. {ch['title']}"
        if ch.get("description"):
            line += f"\n   → {ch['description']}"
        lines.append(line)
    numbered = "\n".join(lines)

    response = interrupt(
        f"Extracted chapters from template:\n\n{numbered}\n\n"
        "Type approval (ok / good / proceed) to start generation, "
        "or enter your modifications (e.g. remove chapter 2, add chapter about X):"
    )

    action = _classify_response(response)
    if action == "approve":
        return {"action": "approve"}
    return {"action": "refine", "feedback": [response]}
