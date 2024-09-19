import cv2
import face_recognition
from face_detection.face_detection_config import FaceDetectionConfig
from utils.logger import JarvisLogger

config = FaceDetectionConfig()

logger = JarvisLogger("FaceDetectionObject")


class FaceDetectionObject:
    def __init__(self):
        self.known_face_path = config.KNOWN_FACE_PATH
        self.known_face = face_recognition.load_image_file(self.known_face_path)
        self.known_face_encoding = face_recognition.face_encodings(self.known_face)[0]

    def detected_face_flow(self):
        return self

    def detect_face(self, rgb_frame):
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([self.known_face_encoding], face_encoding)
                if True in matches:
                    return self.detected_face_flow()

    def passive_capture(self):
        # Start the video capture
        video_capture = cv2.VideoCapture(0)

        while True:
            # Grab a single frame from the video
            ret, frame = video_capture.read()

            # Convert the frame from BGR (OpenCV default) to RGB (face_recognition uses RGB)
            rgb_frame = frame[:, :, ::-1]

            if self.detect_face(rgb_frame):
                break

        # Release the camera and close windows
        video_capture.release()
        cv2.destroyAllWindows()
