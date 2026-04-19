from langgraph.types import interrupt
from graph_state import GraphState


def collect_topic(state: GraphState) -> dict:
    topic = interrupt("ما موضوع الملف؟\n").strip()
    return {"topic": topic}


def collect_doc_type(state: GraphState) -> dict:
    doc_type = interrupt("ما نوع الملف؟ (تقرير / خطة / عرض / دراسة ...)\n").strip()
    return {"doc_type": doc_type}


def collect_chapter_count(state: GraphState) -> dict:
    raw = interrupt("كم فصل تبي؟ (رقم)\n").strip()
    try:
        count = max(1, int(raw))
    except ValueError:
        count = 5
    return {"requested_chapter_count": count}
