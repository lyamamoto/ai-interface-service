import uuid
from sqlalchemy import Column, String, ForeignKey, Index

from app import Base

class Thread(Base):
    __tablename__ = 'threads'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey('customers.id'), index=True)
    source = Column(String)
    source_id = Column(String)

    __table_args__ = (
        Index("threads_customer_id_idx", "customer_id"),
    )

    def __init__(self, id: str, customer_id: str, source: str, source_id: str):
        self.id = id
        self.customer_id = customer_id
        self.source = source
        self.source_id = source_id