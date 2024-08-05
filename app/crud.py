import logging
from sqlalchemy.orm import Session
from models import Customer
from schemas import CustomerCreate, CustomerUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crud_get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def crud_get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Customer).offset(skip).limit(limit).all()

def crud_create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def crud_update_customer(db: Session, customer: CustomerUpdate, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    db_customer.name = customer.name
    db_customer.email = customer.email
    db.commit()
    db.refresh(db_customer)
    return db_customer

def crud_delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    db.delete(db_customer)
    db.commit()
    return db_customer