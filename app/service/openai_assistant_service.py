from dotenv import load_dotenv
from openai import OpenAI
import os
import uuid

from app.model import Message
from app.service import AssistantService, RedisService

load_dotenv()

class OpenAIAssistantService(AssistantService):
    def __init__(self, model: str = "gpt-3.5-turbo-1106"):
        self.__model = model
        self.__client = OpenAI(api_key=os.getenv("openai.api.key"))

        self.__assistant_for_thread = RedisService("openai.assistant_for_thread")
        self.__thread_for_run = RedisService("openai.thread_for_run")

    def create_assistant(self, customer_id: str, name: str, context: str):
        openai_assistant = self.__client.beta.assistants.create(model=self.__model, name=name, instructions=context)
        
        assistant = self._assistant_repository.create(str(uuid.uuid4()), customer_id, "openai", openai_assistant.id)
        return assistant
    
    def start_thread(self, assistant_id: str, customer_id: str):
        assistant = self._assistant_repository.get_by_id(assistant_id)

        openai_thread = self.__client.beta.threads.create()
        self.__assistant_for_thread.set(openai_thread.id, assistant.source_id)

        thread = self._thread_repository.create(str(uuid.uuid4()), customer_id, "openai", openai_thread.id)
        return thread
    
    def get_thread_messages(self, thread_id: str):
        thread = self._thread_repository.get_by_id(thread_id)

        openai_messages = self.__client.beta.threads.messages.list(thread.source_id)

        messages = [Message(openai_message.id, openai_message.role, openai_message.content[0].text.value, openai_message.created_at) for openai_message in openai_messages]
        return messages
    
    def send_message(self, thread_id: str, content: str):
        thread = self._thread_repository.get_by_id(thread_id)

        openai_message = self.__client.beta.threads.messages.create(thread.source_id, role="user", content=content)

        message = Message(openai_message.id, openai_message.role, openai_message.content[0].text.value, openai_message.created_at)
        return message
    
    def run_thread(self, thread_id: str):
        thread = self._thread_repository.get_by_id(thread_id)

        run = self.__client.beta.threads.runs.create(thread.source_id, assistant_id=self.__assistant_for_thread.get(thread.source_id))
        self.__thread_for_run.set(run.id, thread.source_id)

        return run
    
    def get_run_status(self, run_id: str):
        run = self.__client.beta.threads.runs.retrieve(run_id, thread_id=self.__thread_for_run.get(run_id))
        return run.status