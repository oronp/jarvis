import os


class FaceDetectionConfig:
    FACE_DETECTION_DIR: str = os.path.dirname(os.path.abspath(__file__))
    KNOWN_FACE_PATH: str = os.path.join(FACE_DETECTION_DIR, "known_faces")
