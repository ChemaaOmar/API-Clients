from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.main import app
import unittest
import aio_pika
import asyncio
import time
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def wait_for_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            await connection.close()
            break
        except Exception:
            print("Waiting for RabbitMQ...")
            time.sleep(5)


# Configuration du client de test pour utiliser la base de données de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class CustomersAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Attendre que RabbitMQ soit prêt
        loop = asyncio.get_event_loop()
        loop.run_until_complete(wait_for_rabbitmq())

        # Créer les tables de la base de données de test
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Supprimer les tables de la base de données de test
        Base.metadata.drop_all(bind=engine)

    def test_create_customer(self):
        # Tester la création d'un nouveau client
        response = self.client.post(
            "/customers/",
            json={"name": "Clement", "email": "clement@epsi.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Clement")
        self.assertEqual(response.json()["email"], "clement@epsi.com")

    def test_read_customer(self):
        # Tester la lecture d'un client existant
        response = self.client.post(
            "/customers/",
            json={"name": "Paul", "email": "paul@epsi.com"}
        )
        customer_id = response.json()["id"]

        response = self.client.get(f"/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Paul")

    def test_read_nonexistent_customer(self):
        # Tester la lecture d'un client inexistant
        response = self.client.get("/customers/999")
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        # Tester la mise à jour d'un client existant
        response = self.client.post(
            "/customers/",
            json={"name": "Younes", "email": "younes@epsi.com"}
        )
        customer_id = response.json()["id"]

        response = self.client.put(
            f"/customers/{customer_id}",
            json={"name": "Younes Updated", "email": "younes.updated@epsi.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Younes Updated")

    def test_delete_customer(self):
        # Tester la suppression d'un client existant
        response = self.client.post(
            "/customers/",
            json={"name": "Omar", "email": "omar@epsi.com"}
        )
        customer_id = response.json()["id"]

        response = self.client.delete(f"/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)

        # Vérifier que le client a été supprimé
        response = self.client.get(f"/customers/{customer_id}")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
