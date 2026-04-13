"""
Pydantic Schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContentRequest(BaseModel):
    """Schema for content generation request"""
    
    topic: str = Field(..., min_length=3, max_length=255, description="Topic for content generation")


class ContentResponse(BaseModel):
    """Schema for content response"""
    
    id: int
    topic: str
    title: str
    content: str
    meta_title: str
    meta_description: str
    seo_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class GenerateResponse(BaseModel):
    """Schema for generation endpoint response"""
    
    success: bool
    message: str
    data: Optional[ContentResponse] = None
    error: Optional[str] = None


class AllContentResponse(BaseModel):
    """Schema for fetching all content"""
    
    success: bool
    total: int
    data: list[ContentResponse]
