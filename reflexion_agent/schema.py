from pydantic import BaseModel,Field
from typing import List

class Reflection(BaseModel):
    missing:str=Field(description="Critique of what is missing")
    superfluos:str=Field(description="Critique of what is superfluos")

class AnswerQuestion(BaseModel):
    """Answer the question"""
    answer:str=Field("~250 word detailed answer to the question")
    search_queries:List[str]=Field(
        description="1-3 search quries for reseaching improvements to address the critique of your current answer"
    )
    reflection:Reflection=Field(description="Your refelection on initial answer.")

    
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )