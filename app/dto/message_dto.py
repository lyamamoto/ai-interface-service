class MessageDTO:

    id: str
    role: str
    body: str
    created_at: int

    def __init__(self, id: str, role: str, body: str, created_at: int):
        self.id = id
        self.role = role
        self.body = body
        self.created_at = created_at

    def to_json(self):
        return {
            "id": self.id,
            "role": self.role,
            "body": self.body,
            "created_at": self.created_at,
        }