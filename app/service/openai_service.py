from dotenv import load_dotenv
from openai import OpenAI
import os
import redis

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.__client = OpenAI(api_key=os.getenv("openai.api.key"))

        self.__assistant_for_thread = redis.StrictRedis(host=os.getenv("redis.host"), port=os.getenv("redis.port"), db=0)
        self.__thread_for_run = redis.StrictRedis(host=os.getenv("redis.host"), port=os.getenv("redis.port"), db=1)

    def create_assistant(self, name: str, context: str, model: str = "gpt-3.5-turbo-1106"):
        return self.__client.beta.assistants.create(
            model=model,
            name=name,
            instructions=context,
        )

    def get_assistant(self, assistant_id: str):
        return self.__client.beta.assistants.retrieve(assistant_id)
    
    def create_thread(self, assistant_id: str):
        thread = self.__client.beta.threads.create()
        self.__assistant_for_thread.set(thread.id, assistant_id)
        return thread
    
    def get_thread(self, thread_id: str):
        return self.__client.beta.threads.retrieve(thread_id)
    
    def update_thread_assistant(self, thread_id: str, assistant_id: str):
        self.__assistant_for_thread.set(thread_id, assistant_id)
    
    def run_thread(self, thread_id: str):
        run = self.__client.beta.threads.runs.create(thread_id, assistant_id=self.__assistant_for_thread.get(thread_id))
        self.__thread_for_run.set(run.id, thread_id)
        return run
    
    def add_message(self, thread_id: str, content: str, role: str = "user"):
        return self.__client.beta.threads.messages.create(thread_id, role=role, content=content)
    
    def get_messages(self, thread_id: str):
        return self.__client.beta.threads.messages.list(thread_id)
    
    def retrieve_run(self, run_id: str):
        return self.__client.beta.threads.runs.retrieve(run_id, thread_id=self.__thread_for_run.get(run_id))