import uuid
from sqlalchemy import Column, String, ForeignKey

from app import Base

class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey('customers.id'))
    source = Column(String)
    source_id = Column(String)

    def __init__(self, id: str, customer_id: str, source: str, source_id: str):
        self.id = id
        self.customer_id = customer_id
        self.source = source
        self.source_id = source_id