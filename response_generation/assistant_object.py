from openai import OpenAI
from utils.logger import JarvisLogger
from speech_to_text.stt_object import SpeechRecognizerObject


logger = JarvisLogger('assistant')


class AssistantObject:
    openai_client: OpenAI = OpenAI()

    def __init__(self):
        self.stt_object = SpeechRecognizerObject()

    def conversation(self):
        messages = []
        while True:
            try:
                audio = self.stt_object.record_audio()
                response = self.stt_object.recognize_with_whisper(audio)
                logger.info("You said:", response)

            #     if user_input.lower() in ["exit", "quit", "bye"]:
            #         print("Assistant: Goodbye!")
            #         speak_text("Goodbye!")
            #         break
            #
            #     response, messages = generate_response(user_input, messages)
            #     print("Assistant:", response)
            #     speak_text(response)
            #
            except Exception as e:
                print("Error:", str(e))
                # speak_text("Sorry, I didn't catch that.")


if __name__ == '__main__':
    assistant = AssistantObject()
    assistant.conversation()