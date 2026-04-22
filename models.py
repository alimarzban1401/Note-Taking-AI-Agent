from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Note(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., description="The title of the note")
    content: str = Field(..., description="The main text body of the note")
    tags: List[str] = Field(default_factory=list, description="List of categories or tags")
    created_at: Optional[str] = None