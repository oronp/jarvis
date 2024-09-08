import logging

import speech_recognition as sr
from pydantic import Field, ConfigDict

from speech_to_text.speech_to_text_objects.stt_base_object import STTObject

logger = logging.getLogger("SR Object")


class SRObject(STTObject):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    recognizer: sr.Recognizer = Field(default=sr.Recognizer(), description="The recognizer object")

    def recognize_speech_from_microphone(self):

        # Use the microphone as source for input.
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
                recognized_text = self.recognizer.recognize_google_cloud(audio, language=self.language)
                logger.info(f"You said: {recognized_text}")
                return recognized_text

            except sr.UnknownValueError:
                # Speech was unintelligible
                logger.error("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                # Could not request results from Google Speech Recognition service
                logger.error(f"Could not request results; {e}")
                return None
            except sr.WaitTimeoutError:
                # User did not speak in time
                logger.error("Listening timed out while waiting for phrase to start.")
                return None
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return None
