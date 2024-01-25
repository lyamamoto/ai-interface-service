from app import session
from app.model import Customer

class CustomerRepository:
    def create(self, id: str, name: str):
        customer = Customer(id, name)
        session.add(customer)
        session.commit()

    def get_by_id(self, id: str):
        return session.query(Customer).filter_by(id=id).first()

    def get_all(self):
        return session.query(Customer).all()

    def update(self, id: str, name: str):
        customer = session.query(Customer).filter_by(id=id).first()
        customer.name = name
        session.merge(customer)
        session.commit()

    def delete(self, id: str):
        customer = session.query(Customer).filter_by(id=id).first()
        session.delete(customer)
        session.commit()