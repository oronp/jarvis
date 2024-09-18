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
        }
        if task_notes:
            task['notes'] = task_notes
        if due_date:
            task['due'] = due_date.isoformat() + 'Z'  # Due date must be in RFC3339 format

        result = self.service.tasks().insert(tasklist='@default', body=task).execute()
        print(f'Task created: {result["title"]} (ID: {result["id"]})')


if __name__ == '__main__':
    a = GoogleTasksApiObject()
    a.add_task(task_title="Test", task_notes="Test notes")
    print(1)
