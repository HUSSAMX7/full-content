from langgraph.types import interrupt
from graph_state import GraphState



def collect_input(state: GraphState) -> dict:

    response = interrupt("Hello! What is the topic of your document?\n")
    return {
        "topic": response.strip() }