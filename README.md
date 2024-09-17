# API-Clients

# Creation of the shared network
docker network create shared-network

# Build app
docker-compose build

# Run app
docker-compose up

# Stop app
docker-compose down

# Application 

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Postman collection

### JSON File

```json 
{
    "info": {
        "name": "FastAPI Customers API",
        "_postman_id": "your_postman_id",
        "description": "Collection for testing API Customers",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Create Customer",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"name\": \"Clement\", \"email\": \"clement@epsi.com\"}"
                },
                "url": {
                    "raw": "http://127.0.0.1:8000/customers/",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8000",
                    "path": [
                        "customers"
                    ]
                }
            },
            "response": []
        },
        {
            "name": "Get Customer by ID",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://127.0.0.1:8000/customers/:customer_id",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8000",
                    "path": [
                        "customers",
                        ":customer_id"
                    ],
                    "variable": [
                        {
                            "key": "customer_id",
                            "value": "1"
                        }
                    ]
                }
            },
            "response": []
        },
        {
            "name": "Update Customer",
            "request": {
                "method": "PUT",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"name\": \"Younes Updated\", \"email\": \"younes.updated@epsi.com\"}"
                },
                "url": {
                    "raw": "http://127.0.0.1:8000/customers/:customer_id",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8000",
                    "path": [
                        "customers",
                        ":customer_id"
                    ],
                    "variable": [
                        {
                            "key": "customer_id",
                            "value": "1"
                        }
                    ]
                }
            },
            "response": []
        },
        {
            "name": "Delete Customer",
            "request": {
                "method": "DELETE",
                "header": [],
                "url": {
                    "raw": "http://127.0.0.1:8000/customers/:customer_id",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8000",
                    "path": [
                        "customers",
                        ":customer_id"
                    ],
                    "variable": [
                        {
                            "key": "customer_id",
                            "value": "1"
                        }
                    ]
                }
            },
            "response": []
        }
    ]
}
```