from pydantic import BaseModel


class Chapter(BaseModel):
    title: str
    description: str = ""


class ChapterList(BaseModel):
    chapters: list[Chapter]


class ReviewDecision(BaseModel):
    action: str  # "approve", "refine", or "regenerate"
