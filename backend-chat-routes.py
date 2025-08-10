"""
Chat API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Conversation, Message
from app.schemas.chat import (
    ChatMessage, ChatResponse, ConversationCreate, ConversationResponse,
    MessageResponse, ConversationList
)
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService

router = APIRouter()


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new conversation
    """
    conversation = ChatService.create_conversation(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        title=conversation_data.title,
        model=conversation_data.model or current_user.preferred_model
    )
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        model_used=conversation.model_used,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=0
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Get user's conversations
    """
    conversations = ChatService.get_user_conversations(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    
    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            model_used=conv.model_used,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific conversation with messages
    """
    conversation = ChatService.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        model_used=conversation.model_used,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(conversation.messages),
        messages=[
            MessageResponse(
                id=msg.id,
                content=msg.content,
                message_type=msg.message_type,
                model_used=msg.model_used,
                token_count=msg.token_count,
                processing_time=msg.processing_time,
                created_at=msg.created_at,
                metadata=msg.metadata
            )
            for msg in conversation.messages
        ]
    )


@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(
    conversation_id: int,
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message and get AI response
    """
    # Verify conversation belongs to user
    conversation = ChatService.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Save user message
    user_message = ChatService.create_message(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        content=message.content,
        message_type="user"
    )
    
    try:
        # Get AI response
        llm_service = LLMService()
        ai_response = await llm_service.generate_response(
            model=message.model or conversation.model_used,
            messages=ChatService.get_conversation_history(db, conversation_id),
            user_context={
                "user_id": current_user.id,
                "organization_id": current_user.organization_id,
                "role": current_user.role
            }
        )
        
        # Save AI message
        ai_message = ChatService.create_message(
            db=db,
            conversation_id=conversation_id,
            user_id=current_user.id,
            content=ai_response.content,
            message_type="assistant",
            model_used=ai_response.model,
            token_count=ai_response.token_count,
            processing_time=ai_response.processing_time,
            metadata=ai_response.metadata
        )
        
        # Update conversation timestamp
        ChatService.update_conversation_timestamp(db, conversation_id)
        
        return ChatResponse(
            conversation_id=conversation_id,
            message_id=ai_message.id,
            content=ai_response.content,
            model_used=ai_response.model,
            token_count=ai_response.token_count,
            processing_time=ai_response.processing_time,
            metadata=ai_response.metadata
        )
        
    except Exception as e:
        # Log error and return error message
        error_message = ChatService.create_message(
            db=db,
            conversation_id=conversation_id,
            user_id=current_user.id,
            content=f"I apologize, but I encountered an error processing your request: {str(e)}",
            message_type="assistant",
            metadata={"error": True, "error_message": str(e)}
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate AI response"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a conversation
    """
    conversation = ChatService.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    ChatService.delete_conversation(db, conversation_id)
    
    return {"message": "Conversation deleted successfully"}


@router.put("/conversations/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: int,
    title_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update conversation title
    """
    conversation = ChatService.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    new_title = title_update.get("title", "").strip()
    if not new_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
    
    ChatService.update_conversation_title(db, conversation_id, new_title)
    
    return {"message": "Title updated successfully"}


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
):
    """
    Get messages from a specific conversation
    """
    # Verify conversation access
    conversation = ChatService.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = ChatService.get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
        limit=limit,
        offset=offset
    )
    
    return [
        MessageResponse(
            id=msg.id,
            content=msg.content,
            message_type=msg.message_type,
            model_used=msg.model_used,
            token_count=msg.token_count,
            processing_time=msg.processing_time,
            created_at=msg.created_at,
            metadata=msg.metadata
        )
        for msg in messages
    ]