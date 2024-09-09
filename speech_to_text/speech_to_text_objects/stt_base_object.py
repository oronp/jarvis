from pydantic import BaseModel, Field


class STTObject(BaseModel):
    confidence: float = Field(0, description="The confidence of the STT object")
    language: str = Field(..., description="The language of the STT object")
