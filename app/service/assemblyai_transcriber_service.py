from dotenv import load_dotenv
from openai import OpenAI
import os
import uuid

from app.service import TranscriberService

load_dotenv()

class AssemblyAITranscriberService(TranscriberService):

    __source = "openai"

    def __init__(self, transcription_model: str = "whisper-1", tts_model: str = "tts-1"):
        self.__transcription_model = transcription_model
        self.__tts_model = tts_model
        self.__client = OpenAI(api_key=os.getenv("openai.api.key"))

    def transcribe(self, customer_id: str, file: str):
        audio_file = open(file, "rb")
        openai_transcription = self.__client.audio.transcriptions.create(model=self.__transcription_model, file=audio_file)

        transcription = self._transcription_repository.create(str(uuid.uuid4()), customer_id, self.__source, openai_transcription.id)
        return transcription
    
    def translate(self, customer_id: str, file: str):
        audio_file = open(file, "rb")
        openai_translation = self.__client.audio.translations.create(model=self.__transcription_model, file=audio_file)

        translation = self._transcription_repository.create(str(uuid.uuid4()), customer_id, self.__source, openai_translation.id)
        return translation
    
    def generate_speech(self, customer_id: str, text: str):
        openai_speech = self.__client.audio.speech.create(model=self.__tts_model, voice="alloy", input=text)

        return openai_speech