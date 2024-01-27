import uuid
from abc import ABC, abstractmethod

from app.repository import TranscriptionRepository

class TranscriberService(ABC):

    _transcription_repository = TranscriptionRepository()

    @abstractmethod
    def transcribe(self, customer_id: str, file: str):
        pass
    
    @abstractmethod
    def generate_speech(self, customer_id: str, text: str):
        pass

    def get_all_transcriptions_by_customer(self, customer_id: str):
        return self._transcription_repository.get_by_customer_id(customer_id)