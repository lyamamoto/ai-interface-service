import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)

    #assistants = relationship("Assistant", back_populates="customer")
    #threads = relationship("Thread", back_populates="customer")

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name