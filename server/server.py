from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status

from tools_objects import Microphone, Camera, ControlMicrophoneRequest, ControlCameraRequest

API_KEY = "your_secure_api_key"  # Replace with a secure key

app = FastAPI(title="Smart Home AI Assistant Server")


# Authentication dependency
def get_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key


microphones = [
    Microphone(id=1, name="Living Room Mic", status="active"),
    Microphone(id=2, name="Kitchen Mic", status="inactive"),
    Microphone(id=3, name="Bedroom Mic", status="active"),
]

cameras = [
    Camera(id=1, name="Front Door Camera", status="active", recording=False),
    Camera(id=2, name="Lobby Camera", status="inactive", recording=False),
]


# Utility Functions (Replace with actual device control logic)
async def start_camera_recording(camera: Camera):
    # Implement actual start recording logic
    camera.recording = True
    print(f"Camera {camera.id} started recording.")


async def stop_camera_recording(camera: Camera):
    # Implement actual stop recording logic
    camera.recording = False
    print(f"Camera {camera.id} stopped recording.")


async def activate_microphone(mic: Microphone):
    # Implement actual activation logic
    mic.status = "active"
    print(f"Microphone {mic.id} activated.")


async def deactivate_microphone(mic: Microphone):
    # Implement actual deactivation logic
    mic.status = "inactive"
    print(f"Microphone {mic.id} deactivated.")


# API Endpoints

@app.get("/microphones", response_model=List[Microphone])
async def get_microphones(api_key: str = Depends(get_api_key)):
    """
    Retrieve a list of all microphones.
    """
    return microphones


@app.post("/microphones/control")
async def control_microphone(request: ControlMicrophoneRequest, api_key: str = Depends(get_api_key)):
    """
    Control a specific microphone (activate/deactivate).
    """
    mic = next((m for m in microphones if m.id == request.microphone_id), None)
    if not mic:
        raise HTTPException(status_code=404, detail="Microphone not found")

    if request.action == "activate":
        await activate_microphone(mic)
    elif request.action == "deactivate":
        await deactivate_microphone(mic)
    else:
        raise HTTPException(status_code=400, detail="Invalid action for microphone")

    return {"message": f"Microphone {mic.id} {request.action}d successfully."}


@app.get("/cameras", response_model=List[Camera])
async def get_cameras(api_key: str = Depends(get_api_key)):
    """
    Retrieve a list of all cameras.
    """
    return cameras


@app.post("/cameras/control")
async def control_camera(request: ControlCameraRequest, api_key: str = Depends(get_api_key)):
    """
    Control a specific camera (start/stop recording).
    """
    cam = next((c for c in cameras if c.id == request.camera_id), None)
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found")

    if request.action == "start_recording":
        await start_camera_recording(cam)
    elif request.action == "stop_recording":
        await stop_camera_recording(cam)
    else:
        raise HTTPException(status_code=400, detail="Invalid action for camera")

    return {"message": f"Camera {cam.id} {request.action.replace('_', ' ')} successfully."}


@app.get("/microphones/{mic_id}/stream")
async def stream_microphone(mic_id: int, api_key: str = Depends(get_api_key)):
    """
    Stream audio from a specific microphone.
    """
    mic = next((m for m in microphones if m.id == mic_id), None)
    if not mic:
        raise HTTPException(status_code=404, detail="Microphone not found")

    if mic.status != "active":
        raise HTTPException(status_code=400, detail="Microphone is not active")

    # Implement actual streaming logic
    # For example, return an audio stream or link
    return {"message": f"Streaming audio from Microphone {mic.id}."}


@app.get("/cameras/{cam_id}/stream")
async def stream_camera(cam_id: int, api_key: str = Depends(get_api_key)):
    """
    Stream video from a specific camera.
    """
    cam = next((c for c in cameras if c.id == cam_id), None)
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found")

    if cam.status != "active":
        raise HTTPException(status_code=400, detail="Camera is not active")

    # Implement actual streaming logic
    # For example, return a video stream or link
    return {"message": f"Streaming video from Camera {cam.id}."}


@app.post("/ai/command")
async def ai_command(command: str, api_key: str = Depends(get_api_key)):
    """
    Process a command using the AI assistant.
    """
    return {"message": "AI command processing is not yet implemented."}


@app.get("/health")
async def health_check():
    return {"status": "Server is running."}


# Run the server
if __name__ == "__main__":
    uvicorn.run("smart_home_server:app", host="0.0.0.0", port=8000, reload=True)
