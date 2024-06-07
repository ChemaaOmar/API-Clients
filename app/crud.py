from sqlalchemy.orm import Session
import models, schemas

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer: schemas.CustomerUpdate, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    db_customer.name = customer.name
    db_customer.email = customer.email
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    db.delete(db_customer)
    db.commit()
    return db_customer