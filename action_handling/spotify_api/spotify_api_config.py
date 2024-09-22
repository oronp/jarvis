import json
import os

from config.base_config import BaseConfig


class SpotifyApiConfig(BaseConfig):
    SPOTIFY_AUTH_URL: str = os.path.join(BaseConfig.SECRET_DIR, "spotify_api_cred.json")
    SCOPES: list[str] = ['user-read-playback-state',
                         'user-modify-playback-state',
                         'user-read-currently-playing']
    STR_SCOPE: str = ' '.join(SCOPES)

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str

    def __post_init__(self):
        super().__post_init__()
        with open(self.SPOTIFY_AUTH_URL, 'r') as creds_file:
            creds_dict = json.load(creds_file)
        object.__setattr__(self, 'SPOTIFY_CLIENT_ID', creds_dict.get('client_id'))
        object.__setattr__(self, 'SPOTIFY_CLIENT_SECRET', creds_dict.get('client_secret'))
        object.__setattr__(self, 'SPOTIFY_REDIRECT_URI', creds_dict.get('redirect_url'))


if __name__ == '__main__':
    SpotifyApiConfig()