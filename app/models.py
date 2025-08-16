from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class AITaskRequest(BaseModel):
    """Request model for the AI task endpoint"""
    task: str = Field(..., description="Task type: qa, fetch_latest, generate_image, generate_content")
    question: Optional[str] = Field(None, description="Question for Q&A task")
    prompt: Optional[str] = Field(None, description="Prompt for image/content generation")
    platform: Optional[str] = Field(None, description="Platform for content generation (facebook, linkedin, twitter)")

class AITaskResponse(BaseModel):
    """Response model for the AI task endpoint"""
    task: str
    success: bool
    data: Optional[Dict[str, Any]]
    message: str

class TokenRequest(BaseModel):
    """Request model for JWT token generation"""
    username: str
    password: str

class QAEntry(BaseModel):
    """Model for Q&A database entries"""
    id: Optional[int] = None
    question: str
    answer: str
    timestamp: Optional[datetime] = None

class ImageResponse(BaseModel):
    """Model for image generation response"""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    prompt: str

class ContentResponse(BaseModel):
    """Model for content generation response"""
    content: str
    platform: str
    prompt: str