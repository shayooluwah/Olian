"""
Database models for Olian Enterprise LLM Platform
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum

from app.core.database import Base


class UserRole(PyEnum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class TrainingStatus(PyEnum):
    """Training job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Organization(Base):
    """Organization model"""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Settings
    max_users = Column(Integer, default=100)
    max_storage_mb = Column(Integer, default=10000)  # 10GB default
    api_rate_limit = Column(Integer, default=1000)   # Requests per hour
    
    # Relationships
    users = relationship("User", back_populates="organization")
    conversations = relationship("Conversation", back_populates="organization")
    training_jobs = relationship("TrainingJob", back_populates="organization")


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(20), default=UserRole.USER.value)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Organization relationship
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="users")
    
    # User preferences
    preferred_model = Column(String(50), default="gpt-4")
    ui_theme = Column(String(20), default="light")
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")


class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="New Conversation")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    model_used = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    organization = relationship("Organization", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), nullable=False)  # 'user' or 'assistant'
    model_used = Column(String(50))
    token_count = Column(Integer, default=0)
    processing_time = Column(Float, default=0.0)  # Seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Metadata for message context
    metadata = Column(JSON, default={})
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")


class Document(Base):
    """Document model for training data"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String(100), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_error = Column(Text)
    
    # Content metadata
    page_count = Column(Integer)
    word_count = Column(Integer)
    character_count = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    
    # Relationships
    organization = relationship("Organization")
    uploaded_by_user = relationship("User")


class TrainingJob(Base):
    """Model training job"""
    __tablename__ = "training_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String(255), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Job configuration
    base_model = Column(String(100), nullable=False)
    training_data_path = Column(String(500))
    hyperparameters = Column(JSON, default={})
    
    # Job status and progress
    status = Column(String(20), default=TrainingStatus.PENDING.value)
    progress_percentage = Column(Float, default=0.0)
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    
    # Results and metrics
    final_loss = Column(Float)
    validation_accuracy = Column(Float)
    training_metrics = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Error handling
    error_message = Column(Text)
    
    # Model output
    model_path = Column(String(500))
    model_size_mb = Column(Float)
    
    # Relationships
    organization = relationship("Organization", back_populates="training_jobs")
    created_by_user = relationship("User")


class APIKey(Base):
    """API key management for external LLM services"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    service_name = Column(String(50), nullable=False)  # 'openai', 'anthropic', etc.
    encrypted_key = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True))
    
    # Usage tracking
    request_count = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # Relationships
    organization = relationship("Organization")


class AuditLog(Base):
    """Audit logging for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    details = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    