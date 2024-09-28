import json
import os
import queue
import tempfile
from typing import Optional

import openai
import sounddevice as sd
import speech_recognition as sr
from vosk import Model, KaldiRecognizer

from speech_to_text.stt_config import SpeechRecognizerConfig
from utils.logger import JarvisLogger


class SpeechRecognitionError(Exception):
    """Custom exception for speech recognition errors."""
    pass


class SpeechRecognizerObject:
    """
    A class to handle speech recognition using VOSK, Google Cloud Speech-to-Text, and OpenAI Whisper.
    """

    def __init__(self) -> None:
        """
        Initializes the SpeechRecognizer with the given configuration and logger.
        """
        self.config = SpeechRecognizerConfig
        self.logger = JarvisLogger("SpeechRecognizer")
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.vosk_model = self._load_vosk_model(self.config.vosk_model_path)

    def _load_vosk_model(self, model_path: str) -> Model:
        """
        Loads the VOSK model from the specified path.

        Args:
            model_path (str): Path to the VOSK model.

        Returns:
            Model: Loaded VOSK model.

        Raises:
            SpeechRecognitionError: If the model fails to load.
        """
        try:
            self.logger.info(f"Loading VOSK model from {model_path}...")
            model = Model(model_path)
            self.logger.info("VOSK model loaded successfully.")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load VOSK model: {e}")
            raise SpeechRecognitionError(f"Failed to load VOSK model: {e}") from e

    def _queue_callback(self, indata: bytes, frames: int, time_info, status) -> None:
        """
        Callback function for the audio stream to enqueue audio data.

        Args:
            indata (bytes): Input audio data.
            frames (int): Number of frames.
            time_info: Time information.
            status: Status flags.
        """
        if status:
            self.logger.error(f"Stream status: {status}")
        self.audio_queue.put(bytes(indata))

    def record_audio(self) -> str:
        """
        Records audio from the microphone for a specified duration and saves it to a temporary WAV file.

        Returns:
            str: Path to the recorded audio file.

        Raises:
            SpeechRecognitionError: If recording fails.
        """
        try:
            self.logger.info(f"Recording audio for {self.config.record_duration} seconds...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                with sr.Microphone(sample_rate=self.config.sound_sample_rate) as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.record(source, duration=self.config.record_duration)
                    # Save the recorded audio to the temporary file
                    with open(temp_audio_file.name, "wb") as f:
                        f.write(audio.get_wav_data())
                self.logger.info(f"Audio recorded and saved to {temp_audio_file.name}.")
                return temp_audio_file.name
        except Exception as e:
            self.logger.error(f"Failed to record audio: {e}")
            raise SpeechRecognitionError(f"Failed to record audio: {e}") from e

    def recognize_with_google_api(self, audio_file_path: str) -> Optional[str]:
        """
        Recognizes speech using Google Cloud Speech-to-Text API.

        Args:
            audio_file_path (str): Path to the audio file.

        Returns:
            Optional[str]: Recognized text or None if recognition fails.
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                self.logger.info("Processing audio with Google Cloud Speech-to-Text...")
                audio = self.recognizer.record(source)
                recognized_text = self.recognizer.recognize_google_cloud(
                    audio,
                    language=self.config.language,
                    credentials_json=self.config.credentials_json
                )
                self.logger.info(f"Google API recognized: {recognized_text}")
                return recognized_text
        except sr.UnknownValueError:
            self.logger.error("Google API could not understand the audio.")
        except sr.RequestError as e:
            self.logger.error(f"Google API request failed: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred with Google API: {e}")
        return None

    def recognize_with_whisper(self, audio_file_path: str) -> Optional[str]:
        """
        Recognizes speech using OpenAI Whisper API.

        Args:
            audio_file_path (str): Path to the audio file.

        Returns:
            Optional[str]: Recognized text or None if recognition fails.
        """
        try:
            self.logger.info("Processing audio with OpenAI Whisper...")
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            recognized_text = transcript.get("text", "").strip()
            self.logger.info(f"Whisper recognized: {recognized_text}")
            return recognized_text if recognized_text else None
        except Exception as e:
            self.logger.error(f"Whisper API error: {e}")
            return None

    def passive_listen(self) -> Optional[str]:
        """
        Listens passively for specific keywords and triggers corresponding recognition methods.

        Returns:
            Optional[str]: Recognized text based on keyword detection or None.
        """
        try:
            with sd.RawInputStream(
                samplerate=self.config.sound_sample_rate,
                blocksize=self.config.block_size,
                dtype='int16',
                channels=1,
                callback=self._queue_callback
            ):
                self.logger.info("Passive listening started. Press Ctrl+C to stop.")
                recognizer = KaldiRecognizer(self.vosk_model, self.config.sound_sample_rate)

                while True:
                    data = self.audio_queue.get()
                    if recognizer.AcceptWaveform(data):
                        result = recognizer.Result()
                        text = json.loads(result).get("text", "").strip()
                        if text:
                            self.logger.info(f"VOSK recognized: {text}")
                            lowered_text = text.lower()
                            if "hello" in lowered_text:
                                # Record audio and use Google API
                                audio_file = self.record_audio()
                                recognized_text = self.recognize_with_google_api(audio_file)
                                # Clean up the temporary file
                                os.remove(audio_file)
                                return recognized_text
                            elif "whisper" in lowered_text:
                                # Record audio and use Whisper
                                audio_file = self.record_audio()
                                recognized_text = self.recognize_with_whisper(audio_file)
                                # Clean up the temporary file
                                os.remove(audio_file)
                                return recognized_text
                    else:
                        partial_result = recognizer.PartialResult()
                        self.logger.info(f"Partial Result: {partial_result}")
        except KeyboardInterrupt:
            self.logger.info("Passive listening stopped by user.")
        except Exception as e:
            self.logger.error(f"An error occurred during passive listening: {e}")
            raise SpeechRecognitionError(f"Passive listening error: {e}") from e
        return None
