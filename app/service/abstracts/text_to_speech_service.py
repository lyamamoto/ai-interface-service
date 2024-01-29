from abc import ABC, abstractmethod

from app.repository import TranscriptionRepository

class TextToSpeechService(ABC):

    _transcription_repository = TranscriptionRepository()
    
    @abstractmethod
    def generate_speech(self, customer_id: str, text: str):
        pass