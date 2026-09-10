from pydantic import BaseModel
from typing import List


class InputData(BaseModel):
    raw_text: str
    uploaded_files: List[str]
    selected_deliverables: List[str]


class RefinementSettings(BaseModel):
    audience: str
    tone: str


class GeneratedOutput(BaseModel):
    deliverable_type: str
    content: str
