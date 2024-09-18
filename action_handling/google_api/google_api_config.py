import os
from dataclasses import field

from config.base_config import BaseConfig


class GoogleApiConfig(BaseConfig):
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"  # YYYY-MM-DD T HH:MM:SS
    GCP_SCOPES: list = ['https://www.googleapis.com/auth/tasks',
                        'https://www.googleapis.com/auth/calendar']

    OAUTH_JSON_NAME: str = os.path.join(BaseConfig.SECRET_DIR, "oauth_credentials.json")
    OAUTH_TOKEN_JSON_NAME: str = os.path.join(BaseConfig.SECRET_DIR, "oauth_token.json")

    OAUTH_CREDENTIALS_JSON_PATH: str = field(init=False)
    OAUTH_TOKEN_JSON_PATH: str = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, 'OAUTH_CREDENTIALS_JSON_PATH', os.path.join(self.CONFIG_DIR, self.OAUTH_JSON_NAME))
        object.__setattr__(self, 'OAUTH_TOKEN_JSON_PATH', os.path.join(self.CONFIG_DIR, self.OAUTH_TOKEN_JSON_NAME))
