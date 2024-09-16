import json
import os
import pytz
from dataclasses import dataclass, field
from utils.logger import JarvisLogger

logger = JarvisLogger("BaseConfig")


@dataclass(frozen=True)
class BaseConfig:
    google_json_name: str = "jarvis_google_cred.json"
    openai_json_name: str = "open_ai.json"
    oauth_json_name: str = "oauth_credentials.json"
    oauth_token_json_name: str = "oauth_token.json"

    gcp_scopes = ['https://www.googleapis.com/auth/calendar']  # GCP
    local_timezone = pytz.timezone('Asia/Jerusalem')  # Adjust to your location

    google_credentials_json_path: str = field(init=False)
    openai_credentials_json_path: str = field(init=False)
    oauth_credentials_json_path: str = field(init=False)
    oauth_token_json_path: str = field(init=False)

    def __post_init__(self):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        object.__setattr__(self, 'google_credentials_json_path', os.path.join(config_dir, self.google_json_name))
        object.__setattr__(self, 'openai_credentials_json_path', os.path.join(config_dir, self.openai_json_name))
        object.__setattr__(self, 'oauth_credentials_json_path', os.path.join(config_dir, self.oauth_json_name))
        object.__setattr__(self, 'oauth_token_json_path', os.path.join(config_dir, self.oauth_token_json_name))

    def get_google_credentials_json_as_dict(self) -> dict:
        try:
            with open(self.google_credentials_json_path, 'r') as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON from google_credentials_json", params=e)
            return {}

