from pydantic import BaseModel

class MessageDTO(BaseModel):
    id: str
    role: str
    body: str
    created_at: int