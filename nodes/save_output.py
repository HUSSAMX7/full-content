from graph_state import GraphState


def save_output(state: GraphState) -> dict:
    topic = state["topic"]
    chapters = state["generated_chapters"]
    safe_name = topic.replace(" ", "_").replace("/", "_")[:50]
    filename = f"{safe_name}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n")
        for chapter in chapters:
            f.write(chapter)
            f.write("\n\n---\n\n")

    print(f"\nSaved output to: {filename}")
    return {}
