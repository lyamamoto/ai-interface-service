from app import session
from app.model import Thread

class ThreadRepository:
    def create(self, id: str, customer_id: str, source: str, source_id: str):
        thread = Thread(id, customer_id, source, source_id)

        try:
            session.add(thread)
            session.commit()
            session.refresh(thread)
        except Exception:
            session.rollback()

        return thread

    def get_by_id(self, id: str):
        return session.query(Thread).filter_by(id=id).first()

    def get_all(self):
        return session.query(Thread).all()

    def update(self, id: str, source: str, source_id: str):
        thread = session.query(Thread).filter_by(id=id).first()
        thread.source = source
        thread.source_id = source_id

        try:
            session.merge(thread)
            session.commit()
            session.refresh(thread)
        except Exception:
            session.rollback()

        return thread

    def delete(self, id: str):
        thread = session.query(Thread).filter_by(id=id).first()

        try:
            session.delete(thread)
            session.commit()
            session.refresh(thread)
        except Exception:
            session.rollback()