from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import Customer, CustomerCreate, CustomerUpdate
from crud import create_customer, get_customer, get_customers
from database import SessionLocal, engine, Base

# Créer toutes les tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dépendance pour obtenir le DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db=db, customer=customer)

@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/", response_model=list[Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = get_customers(db, skip=skip, limit=limit)
    return customers

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return update_customer(db=db, customer=customer, customer_id=customer_id)

@app.delete("/customers/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return delete_customer(db=db, customer_id=customer_id)