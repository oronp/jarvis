import io
import os
from google.cloud import speech
import speech_recognition as sr
from pydantic import Field, ConfigDict

from speech_to_text.speech_to_text_objects.stt_base_object import STTObject
from utils.logger import JarvisLogger

logger = JarvisLogger("SR_Object")


class SRObject(STTObject):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    recognizer: sr.Recognizer = Field(default=sr.Recognizer(), description="The recognizer object")
    credentials_json: dict = Field(default=os.path.join('config', 'jarvis-435015-e56d7f72b57b.json'),
                                   description="The credentials JSON for Google Cloud Speech-to-Text API")

    # @classmethod
    # @field_validator("credentials_json", mode='before')
    # def validate_credentials_json(cls, value):
    #     try:
    #         value = json.loads('config/jarvis-435015-e56d7f72b57b.json')
    #         return value
    #     except (FileNotFoundError, json.JSONDecodeError):
    #         return {}

    def recognize_speech_from_microphone(self):
        with sr.Microphone() as source:
            logger.info("Adjusting for ambient noise, please wait...")

            # Optional: Adjust the recognizer sensitivity to ambient noise (best practice in noisy environments)
            self.recognizer.adjust_for_ambient_noise(source=source)

            logger.info("Ready to listen, please speak.")

            try:
                # Capture the audio from the microphone
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

                # Use Google's Speech Recognition to convert audio to text
                logger.info("Processing...")
                recognized_text = self.recognizer.recognize_google_cloud(audio, language=self.language,
                                                                         credentials_json=self.credentials_json)

                logger.info(f"You said: {recognized_text}")
                return recognized_text

            except sr.UnknownValueError:
                logger.error("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                logger.error(f"Could not request results; {e}")
                return None
            except sr.WaitTimeoutError:
                logger.error("Listening timed out while waiting for phrase to start.")
                return None
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return None
