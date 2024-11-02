import os
from openai import OpenAI
from openai._legacy_response import HttpxBinaryResponseContent
import pygame
from text_to_speech.tts_config import TTSConfig
from utils.logger import JarvisLogger

config = TTSConfig()

logger = JarvisLogger('TTSObject')


class TTSObject:
    def __init__(self, voice: str = config.Voice.DEFAULT.value):
        self.client = OpenAI()
        self.model = config.Model.TTS_1.value
        self.voice = voice

    def talk(self, text_to_speak: str):
        speech_object = self.text_to_speech_object(text_to_speak)
        self.speech_object_to_file(speech_object)
        self.play_mp3_file()

    def text_to_speech_object(self, text_input: str):
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text_input
        )
        return response

    @staticmethod
    def speech_object_to_file(speech_object: HttpxBinaryResponseContent):
        speech_object.stream_to_file(config.SOUND_FILE_PATH)

    @staticmethod
    def play_mp3_file():
        """Plays an MP3 file using pygame."""
        if os.path.exists(config.SOUND_FILE_PATH):
            # Initialize pygame mixer
            pygame.mixer.init()

            # Load and play the mp3 file
            pygame.mixer.music.load(config.SOUND_FILE_PATH)
            pygame.mixer.music.play()

            # Keep the script alive while audio is playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            logger.error(f"File {config.SOUND_FILE_PATH} not found.")
