from graph_state import GraphState
from schemas import ChapterList
from llm_config import llm
from langchain_core.messages import HumanMessage, SystemMessage

_structured_llm = llm.with_structured_output(ChapterList)

def analyze_template(state: GraphState) -> dict:
    messages = [
        SystemMessage(
            content=(
                "You are an expert document analyst.\n"
                "You receive raw text extracted from a document (e.g. a template). "
                "Read the entire text and infer its logical structure.\n\n"
                "Your task:\n"
                "1) Identify every main section heading from the text itself — "
                "use the wording that actually appears as the section title, not a paraphrase of body content.\n"
                "2) For each heading, attach only text that actually appears in the source as that section's "
                "instructions or body (e.g. bracketed text, or prose directly under/next to the heading).\n"
                "3) Descriptions must be copied or minimally trimmed from the source only — "
                "do not invent, paraphrase, summarize, expand, or add any wording that is not in the input text.\n"
                "4) Keep each title as the heading only; do not merge instructional text into the title.\n"
                "5) If no explicit description exists in the text for a heading, leave description empty.\n"
                "6) Preserve the order headings appear in the source text."
            )
        ),
        HumanMessage(content=f"Template text:\n\n{state['template']}"),
    ]
    result = _structured_llm.invoke(messages)
    return {"chapters": [{"title": c.title, "description": c.description} for c in result.chapters]}