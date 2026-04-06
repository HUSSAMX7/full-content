from pydantic import BaseModel


class Chapter(BaseModel):
    title: str
    description: str = ""


class ChapterList(BaseModel):
    chapters: list[Chapter]
