import asyncio
from io import BufferedReader
from dotenv import load_dotenv
import hashlib
from openai import OpenAI
import os
import uuid

from app.model import Transcription
from app.service.abstracts import SpeechToTextService, TextToSpeechService, TranslationService

load_dotenv()

class OpenAITranscriberService(SpeechToTextService, TextToSpeechService, TranslationService):

    __source = "openai"

    def __init__(self, transcription_model: str = "whisper-1", tts_model: str = "tts-1"):
        self.__transcription_model = transcription_model
        self.__tts_model = tts_model
        self.__client = OpenAI(api_key=os.getenv("openai.api.key"))

    async def __transcribe(self, file: BufferedReader, transcription: Transcription):
        openai_transcription = self.__client.audio.transcriptions.create(model=self.__transcription_model, file=file)
        transcription = self._transcription_repository.update(transcription.id, transcription.file_hash, transcription.source, source_data=openai_transcription.text)

    def transcribe(self, customer_id: str, file_path: str, force_new: bool = False):
        if os.path.exists(file_path) and os.path.isfile(file_path):

            with open(file_path, "rb") as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
                transcription = self._transcription_repository.get_by_file_hash(file_hash, customer_id=customer_id, source=self.__source)

                if force_new or transcription is None or transcription.source_id is None:
                    if transcription is None:
                        transcription = self._transcription_repository.create(str(uuid.uuid4()), customer_id, file_hash, self.__source, None)
                    asyncio.run(self.__transcribe(file, transcription))

                return transcription
        else:
            raise Exception("File not found")
    
    def get_transcription(self, transcription_id: str):
        transcription = self._transcription_repository.get_by_id(transcription_id)
        if transcription is None:
            raise Exception("Transcription not found")
        elif transcription.source_id is None:
            raise Exception("Transcription not ready")
        else:
            openai_transcription = self.__client.audio.transcriptions.retrieve(transcription.source_id)
            return openai_transcription
        
    
    def translate(self, customer_id: str, file: str):
        audio_file = open(file, "rb")
        openai_translation = self.__client.audio.translations.create(model=self.__transcription_model, file=audio_file)

        translation = self._transcription_repository.create(str(uuid.uuid4()), customer_id, self.__source, openai_translation.id)
        return translation
    
    def generate_speech(self, customer_id: str, text: str):
        openai_speech = self.__client.audio.speech.create(model=self.__tts_model, voice="alloy", input=text)

        return openai_speech