# Olian Enterprise LLM Platform Environment Variables

# Basic App Settings
APP_NAME="Olian Enterprise LLM"
DEBUG=False
API_VERSION=v1

# Security Settings
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings (comma-separated list)
ALLOWED_HOSTS=http://localhost:3000,http://127.0.0.1:3000,https://yourdomain.com

# Database Configuration
DATABASE_URL=postgresql://olian_user:olian_password@localhost:5432/olian_db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# LLM API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# File Upload Settings
MAX_UPLOAD_SIZE=52428800  # 50MB in bytes
UPLOAD_DIR=data/uploads
MODELS_DIR=data/models

# Vector Database Settings
CHROMADB_HOST=localhost
CHROMADB_PORT=8001
CHROMADB_COLLECTION_NAME=olian_embeddings

# Celery Configuration (Background Tasks)
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Model Training Settings
MAX_TRAINING_TIME=3600  # 1 hour in seconds

# Logging
LOG_LEVEL=INFO

# Email Settings (Optional - for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Production Settings (Set these in production)
# DATABASE_URL=postgresql://username:password@your-db-host:5432/olian_prod
# REDIS_URL=redis://your-redis-host:6379/0
# ALLOWED_HOSTS=https://your-production-domain.com