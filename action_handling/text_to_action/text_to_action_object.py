import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = "sk-X-NhJUCincTkq8IogBYmGOzZJrHHE4P3LY2U77DRWtT3BlbkFJHLc6gfVoH4UFyARKMdUOHEjWoDEfz1GsKdAkQCwaUA"

openai_client = OpenAI()

# Define possible actions/intents that the assistant can recognize
INTENTS = [
    "set an alarm",
    "play music",
    "check the weather",
    "create a reminder",
    "send a message",
    "call someone",
    "search the web",
    "control smart home devices",
    "get the news",
    "get current time",
]


def detect_intent(user_input):
    try:
        # Provide context about the personal assistant's capabilities to the GPT model
        system_prompt = f"""
        You are a personal assistant. Here are the possible user intentions: {', '.join(INTENTS)}.
        Your response should only contain the user intention without any other words.
        """

        user_prompt = f"""
        Based on the following user input, identify their intention and provide it as one of the listed actions:
        User input: "{user_input}"
        """

        completion = openai_client.chat.completions.create(
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


def handle_intent(intent, user_input):
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


if __name__ == "__main__":
    # Example usage
    user_input = "Can you remind me to buy milk tomorrow?"

    # Detect the user's intent
    detected_intent = detect_intent(user_input)
    print(f"Detected Intent: {detected_intent}")

    # Handle the intent and respond accordingly
    assistant_response = handle_intent(detected_intent, user_input)
    print(f"Assistant: {assistant_response}")

