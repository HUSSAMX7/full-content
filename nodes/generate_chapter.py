from langchain_core.messages import HumanMessage, SystemMessage

from graph_state import GraphState
from llm_config import llm


def generate_chapter(state: GraphState) -> dict:
    idx = state["current_chapter_index"]
    chapter = state["chapters"][idx]
    chapter_title = chapter["title"]
    chapter_description = chapter.get("description", "")
    topic = state["topic"]
    chapter_samples = state["chapter_samples"]
    general_project_context = state["general_project_context"]
    
    # debug print
    print("\n" + "=" * 80)
    print(f"[DEBUG] chapter_samples for chapter: {chapter_title}")
    print(chapter_samples)
    print("=" * 80 + "\n")
    # end debug print

    system_prompt = (
        "You are a specialist technical writer. Write one chapter for a new topic by learning "
        "style and structure from the provided references.\n\n"
        "Strict rules:\n"
        "1) Write only the requested chapter. Do not include other chapters.\n"
        "2) The extracted chapter samples are style/structure guides. Do not copy their project-specific content.\n"
        "3) Keep the output about the new topic only, in the same language as the references.\n"
        "4) If multiple samples are provided, synthesize them into one coherent chapter.\n"
        "5) Resolve conflicts by preferring the most context-relevant and repeated points.\n"
        "6) Do not produce a shallow summary; maintain comparable depth to the reference chapter type.\n"
        "7) Infer structure dynamically from relevant references: if references show multiple themes, "
        "organize the chapter into clear numbered sub-sections; if not, keep it simpler.\n"
        "8) Each sub-section should contain concrete, operational detail (processes, criteria, or examples), "
        "not generic statements.\n"
        "9) Use content from at least two chapter samples when possible, especially for overlapping themes.\n"
        "10) Never mention the source file names, tags, or reference project identity in the final text.\n\n"
        "11) Samples may come from multiple source files. Always merge patterns across samples; do not rely on a single sample.\n\n"
        f"Chapter-matched samples:\n{chapter_samples}\n\n"
        f"General project context:\n{general_project_context}"
    )

    user_prompt = (
        f"New topic: {topic}\n"
        f"Chapter title: {chapter_title}\n"
        f"General project context:\n{general_project_context}"
    )
    if chapter_description:
        user_prompt += f"Chapter description: {chapter_description}\n"
    user_prompt += (
        f"\nTask:\n"
        f"- Produce only the '{chapter_title}' chapter.\n"
        "- First infer a suitable internal outline from the chapter-matched samples, then write the final chapter.\n"
        "- Keep depth comparable to the corresponding reference chapter type.\n"
        "- Prefer synthesis over paraphrased summary.\n"
        "- Do not output planning notes or outline drafts; output final chapter text only."
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)
    draft = f"# {chapter_title}\n\n{response.content}"
    return {"draft": draft}
