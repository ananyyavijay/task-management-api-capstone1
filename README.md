# Task Management API - Cloud Native Capstone

A cloud-native Task Management REST API built using **FastAPI** and deployed on **Microsoft Azure**. The application enables authenticated users to manage projects, tasks, and file attachments while demonstrating modern cloud-native architecture using Azure SQL Database, Azure Blob Storage, Azure Service Bus, Azure Functions, Azure Key Vault, Docker, and GitHub Actions CI/CD.

---

## Live Demo

**API Base URL**

```
https://capstone-task-api.azurewebsites.net
```

**Swagger UI**

```
https://capstone-task-api.azurewebsites.net/docs
```

**ReDoc**

```
https://capstone-task-api.azurewebsites.net/redoc
```

---

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Protected Routes

---

## Project Management

- Create Project
- View Projects
- Update Project
- Delete Project

---

## Task Management

- Create Task
- View Tasks
- Update Task
- Delete Task
- Assign Task
- Filter Tasks

---

## File Attachments

- Upload Attachments
- List Attachments
- Store Files in Azure Blob Storage

---

## Cloud Features

- Azure SQL Database
- Azure Blob Storage
- Azure Service Bus
- Azure Function Consumer
- Azure Key Vault
- Azure App Service
- Docker Deployment
- GitHub Container Registry (GHCR)
- GitHub Actions CI/CD

---

# Architecture

```text
                    Client
                      │
                      ▼
            Azure App Service
             (FastAPI API)
                      │
      ┌───────────────┼─────────────────┐
      │               │                 │
      ▼               ▼                 ▼
Azure SQL      Azure Blob Storage   Azure Service Bus
 Database             │                 │
                      │                 ▼
                      │        Azure Function
                      │                 │
                      └─────────────────▼
                     Application Insights
```

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT Authentication

## Database

- Azure SQL Database

## Cloud

- Azure App Service
- Azure Blob Storage
- Azure Service Bus
- Azure Functions
- Azure Key Vault
- Application Insights

## DevOps

- Docker
- GitHub Actions
- GitHub Container Registry (GHCR)

---

# Project Structure

```
task-management-api-capstone1
│
├── app
│   ├── models
│   ├── routers
│   ├── schemas
│   ├── services
│   ├── dependencies.py
│   ├── database.py
│   └── main.py
│
├── consumer
│   ├── function_app.py
│   ├── host.json
│   ├── requirements.txt
│   └── local.settings.json
│
├── tests
│
├── alembic
│
├── Dockerfile
│
├── requirements.txt
│
└── README.md
```

---

# REST API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | /auth/register |
| POST | /auth/login |
| GET | /users/me |

---

## Projects

| Method | Endpoint |
|---------|----------|
| POST | /projects |
| GET | /projects |
| GET | /projects/{id} |
| PUT | /projects/{id} |
| DELETE | /projects/{id} |

---

## Tasks

| Method | Endpoint |
|---------|----------|
| POST | /tasks |
| GET | /tasks |
| GET | /tasks/{id} |
| PUT | /tasks/{id} |
| DELETE | /tasks/{id} |
| PATCH | /tasks/{id}/assign |

---

## Attachments

| Method | Endpoint |
|---------|----------|
| POST | /tasks/{id}/attachments |
| GET | /tasks/{id}/attachments |

---

# Authentication

The API uses JWT Authentication.

```
Authorization: Bearer <JWT_TOKEN>
```

---

# Azure Blob Storage Workflow

1. User uploads a file.
2. FastAPI receives the request.
3. File is uploaded to Azure Blob Storage.
4. Metadata is stored in Azure SQL Database.
5. Blob URL is returned in the response.

---

# Azure Service Bus Workflow

When a task is assigned:

```
PATCH /tasks/{id}/assign
```

FastAPI

↓

Updates Azure SQL Database

↓

Publishes a JSON message to Azure Service Bus

↓

Azure Function is automatically triggered

↓

Azure Function consumes the message

↓

Logs the notification

↓

Message is removed from the queue

---

# Docker

Build

```bash
docker build -t capstone-task-api .
```

Run

```bash
docker run -p 8000:8000 capstone-task-api
```

---

# Local Setup

Clone repository

```bash
git clone https://github.com/ananyyavijay/task-management-api-capstone1.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run application

```bash
uvicorn app.main:app --reload
```

---

# Environment Variables

| Variable |
|-----------|
| DATABASE_URL |
| JWT_SECRET |
| AZURE_STORAGE_CONNECTION_STRING |
| BLOB_CONTAINER_NAME |
| SERVICE_BUS_CONNECTION |

---

# Azure Services Used

- Azure App Service
- Azure SQL Database
- Azure Blob Storage
- Azure Service Bus
- Azure Functions
- Azure Key Vault
- Application Insights

---

# CI/CD Pipeline

Continuous Integration

- Install dependencies
- Run unit tests
- Verify build

Continuous Deployment

- Build Docker image
- Push image to GitHub Container Registry
- Deploy container to Azure App Service
- Verify deployment

---

# Testing

Run all tests

```bash
pytest tests/ -v
```

---

# Future Improvements

- Email notifications
- Push notifications
- Role-Based Access Control (RBAC)
- Task comments
- Task labels
- Team management
- File versioning
- Email verification
- Password reset
- Rate limiting

---

# Author

**Ananya Vijay**

B.Tech Electronics & Computer Science Engineering

Kalinga Institute of Industrial Technology (KIIT)

GitHub

https://github.com/ananyyavijay

---

# License

This project was developed as part of the Cloud Native Capstone Project.
