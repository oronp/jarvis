import os
from enum import Enum
from config.base_config import BaseConfig


class TTSConfig(BaseConfig):
    TTS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    SOUND_FILE_PATH = os.path.join(TTS_DIR_PATH, 'speech.mp3')

    class Voice(Enum):
        ALLOY = 'alloy'
        ECHO = 'echo'
        FABLE = 'fable'
        ONYX = 'onyx'
        NOVA = 'nova'
        SHIMMER = 'shimmer'
        DEFAULT = ALLOY

    class Model(Enum):
        TTS_1 = 'tts-1'
        TTS_1_HD = 'tts-1-hd'
        DEFAULT = TTS_1

