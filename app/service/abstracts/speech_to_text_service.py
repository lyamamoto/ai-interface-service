from abc import ABC, abstractmethod

from app.repository import TranscriptionRepository

class SpeechToTextService(ABC):

    _transcription_repository = TranscriptionRepository()

    @abstractmethod
    def transcribe(self, customer_id: str, file_path: str):
        pass

    @abstractmethod
    def get_transcription(self, transcription_id: str):
        pass