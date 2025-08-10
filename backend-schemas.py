# app/schemas/auth.py
"""
Authentication schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    organization_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    organization_id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    org_id: Optional[int] = None


# app/schemas/chat.py
"""
Chat schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    model: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: int
    message_id: int
    content: str
    model_used: str
    token_count: int
    processing_time: float
    metadata: Dict[str, Any] = {}


class MessageResponse(BaseModel):
    id: int
    content: str
    message_type: str
    model_used: Optional[str] = None
    token_count: int
    processing_time: float
    created_at: datetime
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    model: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    title: str
    model_used: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    messages: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    conversations: List[ConversationResponse]
    total: int
    offset: int
    limit: int


# app/schemas/user.py
"""
User management schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"
    organization_id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    preferred_model: Optional[str] = None
    ui_theme: Optional[str] = None


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    organization_id: int
    is_active: bool
    preferred_model: str
    ui_theme: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# app/schemas/training.py
"""
Training schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class TrainingStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TrainingJobCreate(BaseModel):
    job_name: str
    base_model: str
    hyperparameters: Optional[Dict[str, Any]] = {}


class TrainingJobResponse(BaseModel):
    id: int
    job_name: str
    organization_id: int
    base_model: str
    status: str
    progress_percentage: float
    current_step: int
    total_steps: int
    hyperparameters: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    training_metrics: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class DocumentUpload(BaseModel):
    filename: str
    file_size: int
    mime_type: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    is_processed: bool
    processing_error: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    character_count: Optional[int] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# app/schemas/organization.py
"""
Organization schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    max_users: Optional[int] = 100
    max_storage_mb: Optional[int] = 10000
    api_rate_limit: Optional[int] = 1000


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_users: Optional[int] = None
    max_storage_mb: Optional[int] = None
    api_rate_limit: Optional[int] = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    max_users: int
    max_storage_mb: int
    api_rate_limit: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True