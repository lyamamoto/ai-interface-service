from app import session
from app.model import Assistant

class AssistantRepository:
    def create(self, id: str, customer_id: str, source: str, source_id: str):
        assistant = Assistant(id, customer_id, source, source_id)

        try:
            session.add(assistant)
            session.commit()
            session.refresh(assistant)
        except Exception:
            session.rollback()

        return assistant

    def get_all(self):
        return session.query(Assistant).all()

    def get_by_id(self, id: str):
        return session.query(Assistant).filter_by(id=id).first()
    
    def get_by_customer_id(self, customer_id: str):
        return session.query(Assistant).filter_by(customer_id=customer_id).all()

    def update(self, id: str, source: str, source_id: str):
        assistant = session.query(Assistant).filter_by(id=id).first()
        assistant.source = source
        assistant.source_id = source_id

        try:
            session.merge(assistant)
            session.commit()
            session.refresh(assistant)
        except Exception:
            session.rollback()

        return assistant

    def delete(self, id: str):
        assistant = session.query(Assistant).filter_by(id=id).first()

        try:
            session.delete(assistant)
            session.commit()
            session.refresh(assistant)
        except Exception:
            session.rollback()