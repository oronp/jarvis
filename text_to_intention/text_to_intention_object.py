from openai import OpenAI
from pydantic import BaseModel, Field

from text_to_intention.text_to_intention_config import TextToIntentionConfig


class TextToIntentionObject(BaseModel):
    openai_client: OpenAI = Field(default=OpenAI(), description="OpenAI client instance")
    intents: list[str] = Field(default=TextToIntentionConfig.INTENTS, description="List of possible intents")

    def detect_intent(self, user_input):
        try:
            # Provide context about the personal assistant's capabilities to the GPT model
            system_prompt = f"""
            You are a personal assistant. Here are the possible user intentions: {', '.join(self.intents)}.
            Your response should only contain the user intention without any other words.
            """

            user_prompt = f"""
            Based on the following user input, identify their intention and provide it as one of the listed actions:
            User input: "{user_input}"
            """

            completion = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )

            # Extract the model's response
            assistant_response = completion.choices[0].message.content
            return assistant_response
        except Exception as e:
            return f"Error occurred: {e}"

    # TODO: change each statement to automation command and finally change this to dict of actions.
    @staticmethod
    def handle_intent(intent):
        # Define actions for various intents
        if "set an alarm" in intent:
            return "Setting an alarm for the specified time."
        elif "play music" in intent:
            return "Playing music based on your preferences."
        elif "check the weather" in intent:
            return "Fetching the current weather information."
        elif "create a reminder" in intent:
            return "Creating a reminder for you."
        elif "send a message" in intent:
            return "Sending your message."
        elif "call someone" in intent:
            return "Calling the specified contact."
        elif "search the web" in intent:
            return "Searching the web for your query."
        elif "control smart home devices" in intent:
            return "Controlling smart home devices."
        elif "get the news" in intent:
            return "Getting the latest news for you."
        elif "get current time" in intent:
            return "The current time is being fetched."
        else:
            return "Sorry, I couldn't understand the request."
