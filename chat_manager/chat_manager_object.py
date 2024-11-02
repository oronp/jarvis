from openai import OpenAI
from utils.logger import JarvisLogger
from chat_manager.history_object import History
from chat_manager_config import ChatManagerConfig

logger = JarvisLogger('ChatManager')


class ChatManager:
    def __init__(self):
        self.chat_history = History()
        self.openai_client = OpenAI()
        self.intents: list[str] = ChatManagerConfig.INTENTS

    def chat_with_ai(self, user_message: str) -> str:
        intention = self.detect_intent(user_message)
        if intention == "play_music":
            return self.play_music(user_message)
        elif intention == "end chat":
            return self.end_chat()
        elif intention == "general_response":
            return self.get_general_response(user_message)

    def get_general_response(self, user_message: str) -> list:
        """
        Get a general response from the assistant.

        Args:
            user_message (str): The user's message.

        Returns:
            str: The assistant's response.
        """
        ai_response = self.openai_client.chat.completions.create(
            model=ChatManagerConfig.GPT_MODEL_MINI,
            messages=self.chat_history.get_history() + [{"role": "user", "content": user_message}]
        )
        self.chat_history.add_entry(user_message, ai_response)
        return self.chat_history.get_history()

    def detect_intent(self, user_input: str) -> str:
        system_prompt = f"""
        You are a personal assistant. Here are the possible user intentions: {', '.join(self.intents)}.
        Your response should only contain the user intention without any other words.
        """

        user_prompt = f"""
        Based on the following user input, identify their intention and provide it as one of the listed actions:
        User input: "{user_input}"
        """

        completion = self.openai_client.chat.completions.create(
            model=ChatManagerConfig.GPT_MODEL_MINI,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        # Extract the model's response
        assistant_response = completion.choices[0].message.content
        return assistant_response

    def play_music(self, user_message: str) -> list:
        """
        Play music based on the user's message.

        Args:
            user_message (str): The user's message.

        Returns:
            str: The assistant's response.
        """
        prompt = f"""
        The user is asking to play a song by a certain artist. Your task is to extract the song name and artist name from their message and respond in JSON format with two keys: "artist" and "song".
        
        Instructions:
        
        If the user explicitly states the name of a song and artist, respond with:
        { "song": "[Song Name]", "artist": "[Artist Name]" }
        If the user only provides the artist name, select one of their popular songs and respond with the same JSON format:
        { "song": "[Song Name]", "artist": "[Artist Name]" }
        Do not play the song; simply respond with the JSON output of the song title and artist name.
        Examples:
        
        User Message: "Play 'Shape of You' by Ed Sheeran."
        Response: { "song": "Shape of You", "artist": "Ed Sheeran" }
        User Message: "Play something by Taylor Swift."
        Response: { "song": "Love Story", "artist": "Taylor Swift" }
        User message: {user_message}
        """
        ai_response = self.openai_client.chat.completions.create(
            model=ChatManagerConfig.GPT_MODEL_MINI,
            messages=self.chat_history.get_history() + [{"role": "user", "content": prompt}]
        )
        self.chat_history.add_entry(user_message, ai_response)
        return self.chat_history.get_history()

    def end_chat(self) -> None:
        self.chat_history.clear_history()

