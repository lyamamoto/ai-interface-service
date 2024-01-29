import uuid
from sqlalchemy import Column, String, ForeignKey, Index

from app import Base

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"))
    file_hash = Column(String, index=True)
    source = Column(String)
    source_id = Column(String)
    source_data = Column(String)

    __table_args__ = (
        Index("transcriptions_customer_id_idx", "customer_id"),
        Index("transcriptions_file_hash_idx", "file_hash"),
    )

    def __init__(self, id: str, customer_id: str, file_hash: str, source: str, source_id: str, source_data: str):
        self.id = id
        self.customer_id = customer_id
        self.file_hash = file_hash
        self.source = source
        self.source_id = source_id
        self.source_data = source_data