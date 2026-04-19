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
                "You receive raw text extracted from a document template. "
                "Read the entire text and extract its chapters/sections.\n\n"
                "Two cases:\n\n"
                "CASE A — Explicit headings exist (a line that is clearly a title, not a full instructional sentence):\n"
                "  • Use the exact heading text as the title.\n"
                "  • The description is the instructional/body text that follows the heading.\n\n"
                "CASE B — No explicit headings (each paragraph is purely instructional text, "
                "i.e. the whole paragraph explains what to write, with no distinct title line):\n"
                "  • Each paragraph or block of text is one chapter.\n"
                "  • Copy the full paragraph text verbatim as the description.\n"
                "  • Infer a SHORT title (1–3 words maximum) that names the core topic of that paragraph. "
                "The title must be a noun/concept label, NOT a phrase copied from the text. "
                "For example, if the paragraph says 'write about the introduction that covers generative AI', "
                "the title should be 'مقدمة' or 'Introduction', not 'introduction about our solution'.\n\n"
                "Rules for both cases:\n"
                "  • Never merge multiple paragraphs/sections into one chapter.\n"
                "  • Preserve the original language.\n"
                "  • Preserve the order sections appear in the source.\n"
                "  • Do not invent description content beyond what is in the source text."
            )
        ),
        HumanMessage(content=f"Template text:\n\n{state['template']}"),
    ]
    result = _structured_llm.invoke(messages)
    return {"chapters": [{"title": c.title, "description": c.description} for c in result.chapters]}