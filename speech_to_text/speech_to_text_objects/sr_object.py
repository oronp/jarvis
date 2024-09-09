import json
import os
import queue

import sounddevice as sd
import speech_recognition as sr
from pydantic import Field, ConfigDict
from vosk import Model, KaldiRecognizer

from speech_to_text.speech_to_text_objects.stt_base_object import STTObject
from utils.logger import JarvisLogger

logger = JarvisLogger("SR_Object")


class SRObject(STTObject):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    recognizer: sr.Recognizer = Field(default_factory=sr.Recognizer, description="The recognizer object")
    credentials_json: dict = Field(default=os.path.join('config', 'jarvis-435015-e56d7f72b57b.json'),
                                   description="The credentials JSON for Google Cloud Speech-to-Text API")
    vosk_model_path: str = Field(default=os.path.join('models', 'vosk-model-small-en-us-0.15'),
                                 description="The path to the VOSK model")
    sound_sample_rate: int = Field(default=16000, description="The sound sample rate")
    q: queue.Queue = Field(default_factory=queue.Queue, description="The queue for audio data")

    vosk_model: Model = Field(default=None, init=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vosk_model = Model(self.vosk_model_path)

    def queue_callback(self, indata, frames, time, status):
        if status:
            logger.info(status)
        self.q.put(bytes(indata))

    def recognize_speech_with_google_api(self):
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

    def passive_listener(self):
        with sd.RawInputStream(samplerate=self.sound_sample_rate, blocksize=16000, dtype='int16', channels=1,
                               callback=self.queue_callback):
            logger.info("Listening... Press Ctrl+C to stop.")
            rec = KaldiRecognizer(self.vosk_model, self.sound_sample_rate)

            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    text = json.loads(result)["text"]
                    if text:
                        logger.info(f"Recognized: {text}")
                        if "hello" in text.lower():
                            self.recognize_speech_with_google_api()
                            break
                else:
                    logger.info(rec.PartialResult())
