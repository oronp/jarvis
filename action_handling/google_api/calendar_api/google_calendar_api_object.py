from datetime import datetime
from typing import Any

import pytz
from googleapiclient.discovery import build

from action_handling.google_api.google_api_config import GoogleApiConfig
from action_handling.google_api.google_api_object import GoogleApiObject
from utils.logger import JarvisLogger

config = GoogleApiConfig()

logger = JarvisLogger("GoogleCalendarApiObject")


class GoogleCalendarApiObject(GoogleApiObject):
    service: Any = None

    def __init__(self) -> None:
        """
        The parent class authenticates the user creds.
        """
        super().__init__()
        self.service = build('calendar', 'v3', credentials=self.creds)

    @staticmethod
    def get_local_time():
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        now_local = now_utc.astimezone(config.LOCAL_TIMEZONE)
        return now_local.isoformat()

    def list_events(self, number_of_events: int = 10) -> list[dict]:
        """List upcoming events on the user's calendar"""
        current_time = self.get_local_time()

        logger.info(f'Getting the upcoming {number_of_events} events')

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
