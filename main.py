import os
from dotenv import load_dotenv
from docx import Document
from langgraph.types import Command
from pypdf import PdfReader

from workflow import create_workflow
from graph_state import GraphState

load_dotenv()

graph = create_workflow()
config = {"configurable": {"thread_id": "1"}}


def _load_docx(path: str) -> str:
    doc = Document(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            parts.append(t)
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells]
            if any(cells):
                parts.append(" | ".join(cells))
    return "\n".join(parts)


def load_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        return "".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        return _load_docx(path)
    raise ValueError(
        f"Unsupported format: {ext or '(no extension)'} — use .pdf or .docx"
    )


def run():
    
    ref_paths = [
        r"C:\Users\hosam\OneDrive\سطح المكتب\قياس\a.docx",
        r"C:\Users\hosam\OneDrive\سطح المكتب\قياس\b.docx",
        r"C:\Users\hosam\OneDrive\سطح المكتب\قياس\c.docx",
    ]
    print("Loading reference files...")

    parts = []

    for p in ref_paths:
        if not os.path.exists(p):
            print(f"Reference file not found: {p}")
            continue
        
        file_text = load_document(p)

        section = (
            f"[SOURCE: {os.path.basename(p)}]\n"
            f"{file_text}\n"
            f"[END SOURCE: {os.path.basename(p)}]"
        )
        parts.append(section)

    if not parts:
        raise ValueError("No valid reference files were loaded.")

    references_content = "\n\n" + ("-" * 80) + "\n\n"
    references_content = references_content.join(parts)

    print(f"Read {len(references_content)} characters from {len(parts)} reference files.")

    template_path = r"C:\Users\hosam\OneDrive\سطح المكتب\تمبلت.docx"
    general_project_context = "the project was in 2000 and the project name is مخدة"
    # Detect mode based on whether template file exists
    if os.path.exists(template_path):
        print("Template found — using template mode.")
        template_text = load_document(template_path)
        mode = "template"
    else:
        print("No template — using manual mode.")
        template_text = ""
        mode = "template"

    initial_state = GraphState(
        references_content=references_content,
        template=template_text,
        general_project_context=general_project_context,
        mode=mode,
        topic="",
        chapters=[],
        current_chapter_index=0,
        draft="",
        feedback=[],
        action="",
        generated_chapters=[],
    )

    result = graph.invoke(initial_state, config=config)

    while True:
        state = graph.get_state(config)

        if not state.next:
            print("\nContent generation finished!")
            break

        interrupts = state.tasks[0].interrupts if state.tasks else []
        if not interrupts:
            break

        prompt_text = interrupts[0].value
        print("\n" + "=" * 60)
        print(prompt_text)
        print("=" * 60)

        user_input = input("\nYour reply: ").strip()
        result = graph.invoke(
            Command(resume=user_input),
            config=config,
        )


if __name__ == "__main__":
    run()
