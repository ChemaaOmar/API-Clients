from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import aio_pika

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import Customer, CustomerCreate, CustomerUpdate
from crud import crud_create_customer, crud_delete_customer, crud_get_customer, crud_get_customers, crud_update_customer
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

# Configuration RabbitMQ
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def get_rabbitmq_connection():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection

async def publish_message(queue_name: str, message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue.name
        )

@app.post("/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = crud_create_customer(db=db, customer=customer)
    await publish_message("customer_created", f"Customer created: {new_customer.id}")
    return new_customer

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/", response_model=list[Customer])
async def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = crud_get_customers(db, skip=skip, limit=limit)
    return customers


@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud_get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    updated_customer = crud_update_customer(db=db, customer=customer, customer_id=customer_id)
    await publish_message("customer_updated", f"Customer updated: {updated_customer.id}")
    return updated_customer

@app.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    deleted_customer = crud_delete_customer(db=db, customer_id=customer_id)
    await publish_message("customer_deleted", f"Customer deleted: {deleted_customer.id}")
    return deleted_customer
