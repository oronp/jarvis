import os.path
import pickle
import pytz
from datetime import datetime
from typing import Any
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import BaseModel, Field, ConfigDict

from config.base_config import BaseConfig
from utils.logger import JarvisLogger

config = BaseConfig()

logger = JarvisLogger("GoogleCalendarApiObject")


class GoogleCalendarApiObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_json: dict = Field(default=config.google_credentials_json_path,
                              description="Credentials for calendar API")

    service: Any = Field(default=None, description="Google Calendar API service")
    max_results: int = Field(default=10, description="Maximum number of events to retrieve")

    def authenticate_google_calendar(self) -> None:
        """Authenticate and return the Google Calendar service"""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(config.oauth_token_json_path):
            with open(config.oauth_token_json_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config.oauth_credentials_json_path, config.gcp_scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(config.oauth_token_json_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def list_events(self):
        """List upcoming events on the user's calendar"""
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        now_local = now_utc.astimezone(config.local_timezone)
        now_iso = now_local.isoformat()

        logger.info('Getting the upcoming {} events'.format(self.max_results))

        events_result = self.service.events().list(calendarId='primary', timeMin=now_iso,
                                                   maxResults=self.max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            logger.info('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


if __name__ == '__main__':
    a = GoogleCalendarApiObject()
    a.authenticate_google_calendar()
    a.list_events()
