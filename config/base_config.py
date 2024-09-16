import json
import os
import pytz
from dataclasses import dataclass, field
from utils.logger import JarvisLogger

logger = JarvisLogger("BaseConfig")
SECRET_DIR = "secrets"


@dataclass(frozen=True)
class BaseConfig:
    GOOGLE_JSON_NAME: str = os.path.join(SECRET_DIR, "jarvis_google_cred.json")
    OPENAI_JSON_NAME: str = os.path.join(SECRET_DIR, "open_ai.json")
    OAUTH_JSON_NAME: str = os.path.join(SECRET_DIR, "oauth_credentials.json")
    OAUTH_TOKEN_JSON_NAME: str = os.path.join(SECRET_DIR, "oauth_token.json")

    GCP_SCOPES = ['https://www.googleapis.com/auth/calendar']  # GCP
    LOCAL_TIMEZONE = pytz.timezone('Asia/Jerusalem')  # Adjust to your location

    GOOGLE_CREDENTIALS_JSON_PATH: str = field(init=False)
    OPENAI_CREDENTIALS_JSON_PATH: str = field(init=False)
    OAUTH_CREDENTIALS_JSON_PATH: str = field(init=False)
    OAUTH_TOKEN_JSON_PATH: str = field(init=False)

    def __post_init__(self):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        object.__setattr__(self, 'GOOGLE_CREDENTIALS_JSON_PATH', os.path.join(config_dir, self.GOOGLE_JSON_NAME))
        object.__setattr__(self, 'OPENAI_CREDENTIALS_JSON_PATH', os.path.join(config_dir, self.OPENAI_JSON_NAME))
        object.__setattr__(self, 'OAUTH_CREDENTIALS_JSON_PATH', os.path.join(config_dir, self.OAUTH_JSON_NAME))
        object.__setattr__(self, 'OAUTH_TOKEN_JSON_PATH', os.path.join(config_dir, self.OAUTH_TOKEN_JSON_NAME))

