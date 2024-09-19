import os
from dataclasses import dataclass, field

import pytz


@dataclass(frozen=True)
class BaseConfig:
    SECRET_DIR: str = "secrets"
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
    GOOGLE_JSON_NAME: str = os.path.join(SECRET_DIR, "jarvis_google_cred.json")

    LOCAL_TIMEZONE = pytz.timezone('Asia/Jerusalem')  # Adjust to your location

    GOOGLE_CREDENTIALS_JSON_PATH: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'GOOGLE_CREDENTIALS_JSON_PATH', os.path.join(self.CONFIG_DIR, self.GOOGLE_JSON_NAME))
