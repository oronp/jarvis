import os.path
import pickle
from datetime import datetime
from typing import Any

import pytz
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import BaseModel, Field, ConfigDict, model_validator

from action_handling.calendar.google_calendar_api_config import GoogleCalendarApiConfig
from utils.logger import JarvisLogger

config = GoogleCalendarApiConfig()

logger = JarvisLogger("GoogleCalendarApiObject")


class GoogleCalendarApiObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_json: dict = Field(default=config.GOOGLE_CREDENTIALS_JSON_PATH,
                              description="Credentials for calendar API")

    service: Any = Field(default=None, description="Google Calendar API service")

    @staticmethod
    def get_local_time():
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        now_local = now_utc.astimezone(config.LOCAL_TIMEZONE)
        return now_local.isoformat()

    @model_validator(mode='after')
    def authenticate_google_calendar(self) -> 'GoogleCalendarApiObject':
        """
        Authenticate and return the Google Calendar service
        The file token.json stores the user's access and refresh tokens, and is created automatically when the
        authorization flow completes for the first time.
        """
        creds = None
        if os.path.exists(config.OAUTH_TOKEN_JSON_PATH):
            with open(config.OAUTH_TOKEN_JSON_PATH, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config.OAUTH_CREDENTIALS_JSON_PATH, config.GCP_SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(config.OAUTH_CREDENTIALS_JSON_PATH, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

        return self

    def list_events(self, number_of_events: int = 10) -> list[dict]:
        """List upcoming events on the user's calendar"""
        current_time = self.get_local_time()

        logger.info('Getting the upcoming {} events'.format(number_of_events))

        events_result = self.service.events().list(calendarId='primary', timeMin=current_time,
                                                   maxResults=number_of_events, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    def create_event(self, summary: str, location: str, start_time: str, end_time: str, description: str = ''):
        """Create a new event on the user's primary calendar, specifying local timezone"""
        start_time_local = config.LOCAL_TIMEZONE.localize(datetime.strptime(start_time, config.TIME_FORMAT))
        end_time_local = config.LOCAL_TIMEZONE.localize(datetime.strptime(end_time, config.TIME_FORMAT))

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time_local.isoformat(),
                'timeZone': config.LOCAL_TIMEZONE.zone,
            },
            'end': {
                'dateTime': end_time_local.isoformat(),
                'timeZone': config.LOCAL_TIMEZONE.zone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f'Event created: {event.get("htmlLink")}')
