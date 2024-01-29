from abc import ABC, abstractmethod

from app.repository import TranscriptionRepository

class TranslationService(ABC):

    _transcription_repository = TranscriptionRepository()
    
    @abstractmethod
    def translate(self, customer_id: str, file: str):
        pass