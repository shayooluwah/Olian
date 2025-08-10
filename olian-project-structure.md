# Olian - Enterprise LLM Platform Directory Structure

```
Olian/
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── frontend/                          # React TypeScript Frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   └── MessageInput.tsx
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── ConversationList.tsx
│   │   │   ├── Settings/
│   │   │   │   ├── APIConfig.tsx
│   │   │   │   ├── DataTraining.tsx
│   │   │   │   └── SecuritySettings.tsx
│   │   │   └── Layout/
│   │   │       ├── Header.tsx
│   │   │       └── MainLayout.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── chat.ts
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   ├── chat.ts
│   │   │   └── api.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   └── helpers.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useChat.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── backend/                           # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Configuration settings
│   │   ├── dependencies.py           # Common dependencies
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Authentication routes
│   │   │   ├── chat.py              # Chat endpoints
│   │   │   ├── users.py             # User management
│   │   │   ├── training.py          # Model training endpoints
│   │   │   └── admin.py             # Admin functions
│   │   │
│   │   ├── core/                     # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # JWT, password hashing
│   │   │   ├── database.py          # Database connection
│   │   │   └── config.py            # App configuration
│   │   │
│   │   ├── models/                   # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model
│   │   │   ├── conversation.py      # Chat conversations
│   │   │   ├── organization.py      # Organization model
│   │   │   └── training.py          # Training job model
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Auth request/response
│   │   │   ├── chat.py              # Chat schemas
│   │   │   ├── user.py              # User schemas
│   │   │   └── training.py          # Training schemas
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # Authentication logic
│   │   │   ├── chat_service.py      # Chat processing
│   │   │   ├── llm_service.py       # LLM API integrations
│   │   │   ├── training_service.py  # Model training
│   │   │   ├── document_service.py  # Document processing
│   │   │   └── vector_service.py    # Vector database operations
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── file_processing.py   # Document parsing
│   │   │   ├── embeddings.py        # Text embeddings
│   │   │   └── validators.py        # Input validation
│   │   │
│   │   └── workers/                  # Background tasks
│   │       ├── __init__.py
│   │       ├── celery_app.py        # Celery configuration
│   │       └── training_tasks.py    # Training background jobs
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── tests/                        # Test files
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_chat.py
│   │   └── test_training.py
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── Dockerfile
│
├── data/                             # Data storage
│   ├── uploads/                      # Uploaded documents
│   ├── models/                       # Trained model files
│   └── embeddings/                   # Vector embeddings
│
├── scripts/                          # Deployment scripts
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
│
├── docs/                            # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
│
└── infrastructure/                   # Infrastructure as code
    ├── docker/
    │   ├── Dockerfile.frontend
    │   ├── Dockerfile.backend
    │   └── Dockerfile.worker
    ├── k8s/                         # Kubernetes manifests
    │   ├── namespace.yml
    │   ├── deployment.yml
    │   └── service.yml
    └── terraform/                   # Terraform configs
        ├── main.tf
        └── variables.tf
```

## Key Files Explanation

### Frontend Structure
- **components/**: Modular React components organized by feature
- **services/**: API communication layer
- **types/**: TypeScript type definitions
- **hooks/**: Custom React hooks for state management

### Backend Structure
- **api/**: FastAPI route handlers organized by domain
- **core/**: Core functionality like security and database
- **models/**: SQLAlchemy database models
- **schemas/**: Pydantic models for request/response validation
- **services/**: Business logic separated from API handlers
- **workers/**: Background task processing with Celery

### Data & Infrastructure
- **data/**: Local data storage for development
- **scripts/**: Automation and deployment scripts
- **infrastructure/**: Docker and Kubernetes configurations

## Development Workflow
1. Frontend runs on `http://localhost:3000`
2. Backend API runs on `http://localhost:8000`
3. Database runs on `localhost:5432` (PostgreSQL)
4. Redis runs on `localhost:6379` (for caching and Celery)
5. Vector database (ChromaDB) runs on `localhost:8001`

## Next Steps
1. Set up the backend Python environment
2. Create database models and migrations
3. Implement authentication and chat services
4. Connect frontend to backend APIs
5. Add document processing and training capabilities