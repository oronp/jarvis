from pydantic import BaseModel

class Microphone(BaseModel):
    id: int
    name: str
    status: str  # e.g., "active", "inactive"


class Camera(BaseModel):
    id: int
    name: str
    status: str  # e.g., "active", "inactive"
    recording: bool


class ControlCameraRequest(BaseModel):
    camera_id: int
    action: str  # e.g., "start_recording", "stop_recording"


class ControlMicrophoneRequest(BaseModel):
    microphone_id: int
    action: str  # e.g., "activate", "deactivate"