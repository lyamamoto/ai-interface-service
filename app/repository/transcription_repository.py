from app import session
from app.model import Transcription

class TranscriptionRepository:
    def create(self, id: str, customer_id: str, file_hash: str, source: str, source_id: str):
        transcription = Transcription(id, customer_id, file_hash, source, source_id)

        try:
            session.add(transcription)
            session.commit()
            session.refresh(transcription)
        except Exception:
            session.rollback()

        return transcription

    def get_by_id(self, id: str):
        return session.query(Transcription).filter_by(id=id).first()
    
    def get_by_file_hash(self, file_hash: str, customer_id: str | None = None, source: str | None = None):
        query = session.query(Transcription).filter_by(file_hash=file_hash)
        if customer_id is not None:
            query = query.filter_by(customer_id=customer_id)
        if source is not None:
            query = query.filter_by(source=source)
        return query.first()

    def get_all(self):
        return session.query(Transcription).all()

    def update(self, id: str, file_hash: str, source: str, source_id: str | None = None, source_data: str | None = None):
        transcription = session.query(Transcription).filter_by(id=id).first()

        if transcription is not None:
            transcription.file_hash = file_hash
            transcription.source = source
            if source_id is not None:
                transcription.source_id = source_id
            if source_data is not None:
                transcription.source_data = source_data
        else:
            return Transcription(id, "", file_hash, source, source_id)

        try:
            session.merge(transcription)
            session.commit()
            session.refresh(transcription)
        except Exception:
            session.rollback()

        return transcription

    def delete(self, id: str):
        try:
            transcription = session.query(Transcription).filter_by(id=id).first()

            session.delete(transcription)
            session.commit()
            session.refresh(transcription)
        except Exception:
            session.rollback()