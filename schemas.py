from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    # The shape of the JSON the API accepts when creating a student.
    # Spaces at both ends are trimmed before the rules are checked.
    model_config = ConfigDict(str_strip_whitespace=True)

    # Required text, between 1 and 50 characters
    name: str = Field(min_length=1, max_length=50)

class GradeCreate(BaseModel):
    # The shape of the JSON for a new grade: a number from 0 to 100
    score: float = Field(ge=0, le=100)