import json
import os
from utils.logger import JarvisLogger

logger = JarvisLogger("BaseConfig")


class BaseConfig:
    google_json_name: str = "jarvis-435015-e56d7f72b57b.json"
    google_credentials_json_path: dict

    def __init__(self):
        self.get_google_credentials_json_path()

    @classmethod
    def get_google_credentials_json_path(cls):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        cls.google_credentials_json_path = os.path.join(config_dir, cls.google_json_name)

    @classmethod
    def get_google_credentials_json_as_dict(cls):
        try:
            return json.loads(cls.google_credentials_json_path)
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON from google_credentials_json", params=e)

