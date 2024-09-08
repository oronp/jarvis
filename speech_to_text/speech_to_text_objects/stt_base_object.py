from pydantic import BaseModel, Field


class STTObject(BaseModel):
    # text: str = Field(..., description="The text of the STT object")
    # start: float = Field(..., description="The start time of the STT object")
    # end: float = Field(..., description="The end time of the STT object")
    confidence: float = Field(0, description="The confidence of the STT object")
    # duration: float = Field(..., description="The duration of the STT object")
    language: str = Field(..., description="The language of the STT object")
    # speaker: str = Field(default="No Speaker", description="The speaker of the STT object")

