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
                "Analyze the following template and extract all main sections/chapters.\n\n"
                "Rules:\n"
                "1) Identify every main heading/title in the template.\n"
                "2) If a description exists (in brackets [], parentheses, or as text below the heading), "
                "extract it exactly as written.\n"
                "3) If NO description exists for a heading, leave it empty. "
                "4) Preserve the original order of sections.\n"
            )
        ),
       
        HumanMessage(content=f"Template:\n{state['template']}"),
    ]
    
    result = _structured_llm.invoke(messages)

    return {"chapters": [{"title": c.title, "description": c.description} for c in result.chapters]}

