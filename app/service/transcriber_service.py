import uuid
from abc import ABC, abstractmethod

from app.repository import AssistantRepository, ThreadRepository

class TranscriberService(ABC):

    _assistant_repository = AssistantRepository()
    _thread_repository = ThreadRepository()

    @abstractmethod
    def create_assistant(self, customer_id: str, name: str, context: str):
        pass
    
    def get_all_assistants_by_customer(self, customer_id: str):
        return self._assistant_repository.get_by_customer_id(customer_id)

    def get_assistant_by_name(self, customer_id: str, name: str):
        return self._assistant_repository.get_by_name_and_customer_id(customer_id, name)

    @abstractmethod
    def start_thread(self, assistant_id: str, customer_id: str):
        pass
    
    @abstractmethod
    def get_thread_messages(self, thread_id: str):
        pass
    
    @abstractmethod
    def send_message(self, thread_id: str, content: str):
        pass
    
    @abstractmethod
    def run_thread(self, thread_id: str):
        pass
    
    @abstractmethod
    def get_run_status(self, run_id: str):
        pass