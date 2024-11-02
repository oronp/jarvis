from typing import Optional
from utils.logger import JarvisLogger

logger = JarvisLogger('history')


class History:
    """
    A class to manage the conversation history.
    """

    def __init__(self, chat_history: Optional[list[list]] = None):
        """
        Initialize the History class.

        Args:
            chat_history (list[list], optional): A list of two-element lists representing user and bot messages from Gradio.
        """
        self.history = []
        for single_message in chat_history:
            self.add_entry(single_message[0], single_message[1])

    def add_entry(self, user_message: str, bot_message: str) -> None:
        """
        Add a message pair to the conversation history.

        Args:
            user_message (str): The user's message.
            bot_message (str): The bot's response.
        """
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": bot_message})

    def get_history(self) -> list:
        """
        Get the conversation history.

        Returns:
            list: The conversation history.
        """
        return self.history

    def clear_history(self) -> None:
        """
        Clear the conversation history.
        """
        self.history = []
        logger.info("chat history cleared...")
