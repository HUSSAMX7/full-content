from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from llm_config import llm


class ReviewDecision(BaseModel):
    action: str  # "approve" or "refine"


_structured_llm = llm.with_structured_output(ReviewDecision)


def _classify_response(user_response: str) -> str:
    messages = [
        SystemMessage(
            content=(
                "You are a text classifier. Determine the user's intent from their reply to a written chapter.\n"
                "If the reply expresses approval or satisfaction (e.g. ok, good, great, perfect, approved, "
                "looks good, nice, excellent, fine, correct, yes, suitable, accepted...) → action = approve\n"
                "If the reply contains notes, criticism, or a request for changes → action = refine"
            )
        ),
        HumanMessage(content=f'User reply: "{user_response}"'),
    ]
    result: ReviewDecision = _structured_llm.invoke(messages)
    return result.action
