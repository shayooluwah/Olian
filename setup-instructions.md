# Olian Enterprise LLM Platform

A secure, enterprise-ready LLM platform that allows organizations to deploy AI assistants while maintaining complete control over their data and ensuring compliance with security policies.

## 🚀 Features

- **Multi-LLM Support**: OpenAI GPT, Anthropic Claude, and local models
- **Enterprise Security**: Data isolation, encryption, audit logging
- **Document Training**: Upload and train on company-specific documents
- **Role-Based Access**: Admin, user, and viewer roles
- **Conversation Management**: Persistent chat history and organization
- **API Management**: Secure key storage and usage tracking

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   React     │    │   FastAPI   │    │ PostgreSQL  │
│  Frontend   │◄──►│   Backend   │◄──►│  Database   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Redis     │◄──►│   Celery    │    │  ChromaDB   │
│   Cache     │    │   Workers   │    │   Vector    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)
- Git

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url> Olian
cd Olian
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations
nano .env
```

**Required Environment Variables:**
```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://olian_user:olian_password@localhost:5432/olian_db
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
```

### 3. Start with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Task Monitor**: http://localhost:5555 (Celery Flower)

### 5. Create First Organization & User

```bash
# Access the backend container
docker-compose exec backend bash

# Run the setup script
python scripts/create_admin.py
```

## 🏃‍♂️ Local Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Background Workers

```bash
cd backend

# Start Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Start Celery flower (monitoring)
celery -A app.workers.celery_app flower
```

## 🔧 Configuration

### Database Setup

```bash
# Create database (if not using Docker)
createdb olian_db

# Run migrations
cd backend
alembic upgrade head
```

### API Keys Configuration

Add your LLM provider API keys to the `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# For local models (Ollama example)
# No API key needed, just ensure Ollama is running on localhost:11434
```

### Vector Database

ChromaDB is used for document embeddings and similarity search:

```bash
# ChromaDB will start automatically with Docker Compose
# Access at: http://localhost:8001
```

## 📊 Usage

### 1. User Registration

Users can register through the web interface or be created by administrators:

```python
# Via API
POST /api/auth/register
{
    "username": "john_doe",
    "email": "john@company.com",
    "password": "secure_password",
    "full_name": "John Doe",
    "organization_id": 1
}
```

### 2. Document Upload

Upload company documents for training:

```bash
# Via web interface: Settings > Data Training > Upload Files
# Supported formats: PDF, DOCX, TXT, CSV
```

### 3. Chat Interface

Start conversations with AI assistants:

- Create new conversations
- Select different LLM models
- Access conversation history
- Export conversations

### 4. Model Training

Train custom models on your data:

```bash
# Via API or web interface
POST /api/training/jobs
{
    "job_name": "Company Knowledge Base",
    "base_model": "gpt-3.5-turbo",
    "hyperparameters": {...}
}
```

## 🔐 Security Features

### Data Protection
- **Encryption**: All data encrypted in transit and at rest
- **Isolation**: Complete data isolation between organizations
- **Access Control**: Role-based permissions system

### Audit