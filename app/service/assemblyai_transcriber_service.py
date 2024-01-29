from dotenv import load_dotenv
import assemblyai
import assemblyai.api
import hashlib
import os
import uuid

from app.service.abstracts import SpeechToTextService

load_dotenv()

class AssemblyAITranscriberService(SpeechToTextService):

    __source = "assemblyai"

    def __init__(self, speaker_labels: bool | None = True, language_code: assemblyai.LanguageCode | None = "pt"):
        assemblyai.settings.api_key = os.getenv("assemblyai.api.key")
        self.__client = assemblyai.Client(settings=assemblyai.settings)
        self.__config = assemblyai.TranscriptionConfig(speaker_labels=speaker_labels, language_code=language_code)
        self.__transcriber = assemblyai.Transcriber(config=self.__config)

    def transcribe(self, customer_id: str, file_path: str, force_new: bool = False):
        if os.path.exists(file_path) and os.path.isfile(file_path):

            with open(file_path, "rb") as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
                transcription = self._transcription_repository.get_by_file_hash(file_hash, customer_id=customer_id, source=self.__source)

                if force_new or transcription is None or transcription.source_id is None:
                    if transcription is None:
                        transcription = self._transcription_repository.create(str(uuid.uuid4()), customer_id, file_hash, self.__source, None)
                    assemblyai_transcription = self.__transcriber.transcribe_async(file_path, config=self.__config)
                    assemblyai_transcription.add_done_callback(lambda assemblyai_transcription: self._transcription_repository.update(transcription.id, transcription.file_hash, transcription.source, source_id=assemblyai_transcription.result().id))

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
            assemblyai_transcription_response = assemblyai.api.get_transcript(self.__client.http_client, transcription.source_id)
            assemblyai_transcription = assemblyai.Transcript.from_response(client=self.__client, response=assemblyai_transcription_response)
            return assemblyai_transcription