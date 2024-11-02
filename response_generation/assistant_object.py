from openai import OpenAI
from utils.logger import JarvisLogger
from speech_to_text.stt_object import SpeechRecognizerObject
from chat_manager.chat_manager_object import ChatManager
from text_to_speech.tts_object import TTSObject

logger = JarvisLogger('assistant')


class AssistantObject:
    openai_client: OpenAI = OpenAI()

    def __init__(self):
        self.stt_object = SpeechRecognizerObject()
        self.tts_object = TTSObject()

    def conversation(self):
        chat_manager = ChatManager()
        while True:
            try:
                audio = self.stt_object.record_audio()
                user_input = self.stt_object.recognize_with_whisper(audio)
                ai_response = chat_manager.chat_with_ai(user_input)
                self.tts_object.talk(ai_response)

            except Exception as e:
                logger.error("Error:", str(e))

