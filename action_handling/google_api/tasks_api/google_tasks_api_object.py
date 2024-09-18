from datetime import datetime
from typing import Any

from googleapiclient.discovery import build

from action_handling.google_api.google_api_object import GoogleApiObject
from action_handling.google_api.tasks_api.google_tasks_api_config import GoogleTasksApiConfig
from utils.logger import JarvisLogger

config = GoogleTasksApiConfig()

logger = JarvisLogger("GoogleTasksApiObject")


class GoogleTasksApiObject(GoogleApiObject):
    service: Any = None

    def __init__(self):
        super().__init__()
        self.service = build('tasks', 'v1', credentials=self.creds)

    def add_task(self, task_title: str, task_notes: str = None, due_date: datetime = None):
        """Adds a task to Google Tasks."""
        task = {
            'title': task_title,
            'notes': task_notes,
            'due': due_date.isoformat() + 'Z' if due_date else None  # Due date must be in RFC3339 format
        }

        result = self.service.tasks().insert(tasklist='@default', body=task).execute()
        logger.info(f'Task created: {result["title"]} (ID: {result["id"]})')

    def list_tasks(self):
        """Lists all tasks in Google Tasks."""
        return self.service.tasks().list(tasklist='@default').execute()
