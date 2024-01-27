from app import session
from app.model import Transcription

class TranscriptionRepository:
    def create(self, id: str, customer_id: str, source: str, source_id: str):
        transcription = Transcription(id, customer_id, source, source_id)

        try:
            session.add(transcription)
            session.commit()
        except Exception:
            session.rollback()

        return transcription

    def get_by_id(self, id: str):
        return session.query(Transcription).filter_by(id=id).first()

    def get_all(self):
        return session.query(Transcription).all()

    def update(self, id: str, source: str, source_id: str):
        transcription = session.query(Transcription).filter_by(id=id).first()
        transcription.source = source
        transcription.source_id = source_id

        try:
            session.merge(transcription)
            session.commit()
        except Exception:
            session.rollback()

        return transcription

    def delete(self, id: str):
        transcription = session.query(Transcription).filter_by(id=id).first()

        try:
            session.delete(transcription)
            session.commit()
        except Exception:
            session.rollback()