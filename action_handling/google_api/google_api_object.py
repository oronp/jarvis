import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from action_handling.google_api.google_api_config import GoogleApiConfig

config = GoogleApiConfig()


class GoogleApiObject:
    config_json: dict = config.GOOGLE_CREDENTIALS_JSON_PATH

    creds: Credentials

    def __init__(self) -> None:
        """
        Authenticate and return the Google Calendar service
        The file token.json stores the user's access and refresh tokens, and is created automatically when the
        authorization flow completes for the first time.
        """
        if os.path.exists(config.OAUTH_TOKEN_JSON_PATH):
            with open(config.OAUTH_TOKEN_JSON_PATH, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config.OAUTH_CREDENTIALS_JSON_PATH,
                                                                 config.GCP_SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(config.OAUTH_CREDENTIALS_JSON_PATH, 'wb') as token:
                pickle.dump(self.creds, token)
