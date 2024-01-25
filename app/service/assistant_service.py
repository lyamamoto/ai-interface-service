import uuid

from app.model import Assistant, Thread
from app.repository import AssistantRepository, ThreadRepository
from app.service import OpenAIService

class AssistantService:
    def __init__(self):
        # Repositories
        self.__assistant_repository = AssistantRepository()
        self.__thread_repository = ThreadRepository()

        # Services
        self.__openai_service = OpenAIService()

    def create_assistant(self, customer_id: str, name: str, context: str):
        openai_assistant = self.__openai_service.create_assistant(name, context)
        assistant = self.__assistant_repository.create(str(uuid.uuid4()), customer_id, "openai", openai_assistant.id)
        return assistant
    
    def get_all_assistants_by_customer(self, customer_id: str):
        return self.__assistant_repository.get_by_customer_id(customer_id)

    def get_assistant_by_name(self, customer_id: str, name: str):
        return self.__assistant_repository.get_by_name_and_customer_id(customer_id, name)
    
    def start_thread(self, assistant_id: str, customer_id: str):
        assistant = self.__assistant_repository.get_by_id(assistant_id)
        openai_thread = self.__openai_service.create_thread(assistant.source_id)
        thread = self.__thread_repository.create(str(uuid.uuid4()), customer_id, "openai", openai_thread.id)
        return thread
    
    def send_message(self, thread_id: str, message: str):
        return self.__openai_service.add_message(thread_id, message)
    
    def send_message_and_run(self, thread_id: str, message: str):
        message = self.send_message(thread_id, message)
        return self.__openai_service.run_thread(thread_id)
    
    def get_thread_messages(self, thread_id: str):
        return self.__openai_service.get_messages(thread_id).data