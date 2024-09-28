import os
from config.base_config import BaseConfig
from dataclasses import field


class SpeechRecognizerConfig(BaseConfig):
    """Configuration settings for the SpeechRecognizer."""
    language: str = "en-US"
    vosk_model_path: str = os.path.join(BaseConfig.BASE_DIR, 'models', 'vosk-model-small-en-us-0.15')

    sound_sample_rate: int = 16000
    block_size: int = 16000
    record_duration: int = 5