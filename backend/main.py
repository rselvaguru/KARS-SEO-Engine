"""
KARS SEO Engine - FastAPI Backend
AI-powered SEO automation system with local LLM
"""

import os
import logging
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from db.database import init_db, get_db
from models.content_model import Content
from schemas.content_schema import (
    ContentRequest,
    ContentResponse,
    GenerateResponse,
    AllContentResponse
)
from services.content_service import ContentService
from services.seo_service import SEOService
from services.keyword_service import KeywordService
from services.pipeline_service import PipelineService
from services.vector_service import VectorService
from ai.ollama_client import ollama_client
from utils.helpers import truncate_text

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="KARS SEO Engine",
    description="AI-powered SEO automation system using local LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on app startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    
    # Check Ollama availability
    if ollama_client.is_available():
        logger.info(f"✓ Ollama is available (Model: {ollama_client.model})")
    else:
        logger.warning("⚠ Ollama is not available. Ensure Ollama is running on localhost:11434")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    ollama_status = "available" if ollama_client.is_available() else "unavailable"
    return {
        "status": "healthy",
        "service": "KARS SEO Engine",
        "ollama": ollama_status
    }


# Generate content endpoint
@app.post("/generate", response_model=GenerateResponse)
async def generate_content(
    request: ContentRequest,
    db: Session = Depends(get_db)
):
    """
    Generate SEO-optimized content for a given topic
    
    Args:
        request: ContentRequest with topic
        db: Database session
        
    Returns:
        Generated content with SEO metadata
    """
    logger.info(f"Request to generate content for topic: {request.topic}")
    
    try:
        # Check Ollama availability
        if not ollama_client.is_available():
            logger.error("Ollama service not available")
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available. Please ensure Ollama is running."
            )
        
        # Generate content with linking (pass db_session for internal link generation)
        content_result = ContentService.generate_content(request.topic, db_session=db)
        
        if not content_result.get("success"):
            logger.error(f"Content generation failed: {content_result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=content_result.get("error", "Failed to generate content")
            )
        
        generated_title = content_result.get("title")
        generated_content = content_result.get("content")
        
        # Generate SEO metadata
        seo_meta = ContentService.generate_title_and_description(
            request.topic,
            generated_content[:200]
        )
        
        meta_title = seo_meta.get("title")
        meta_description = seo_meta.get("description")
        
        # Calculate SEO score (enhanced scoring)
        seo_score = SEOService.calculate_seo_score(
            request.topic,
            meta_title,
            generated_content,
            meta_description
        )
        
        # Save to database
        db_content = Content(
            topic=request.topic,
            title=generated_title,
            content=generated_content,
            meta_title=meta_title,
            meta_description=meta_description,
            seo_score=seo_score
        )
        
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        
        logger.info(f"Content generated and saved - ID: {db_content.id}, Score: {seo_score}")
        
        return GenerateResponse(
            success=True,
            message=f"Content generated successfully with SEO score: {seo_score}",
            data=ContentResponse.from_orm(db_content)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Get all content endpoint
@app.get("/content", response_model=AllContentResponse)
async def get_all_content(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Fetch all generated content with pagination
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of all content with pagination
    """
    logger.info(f"Fetching content - skip: {skip}, limit: {limit}")
    
    try:
        # Get total count
        total = db.query(Content).count()
        
        # Fetch content
        contents = db.query(Content).offset(skip).limit(limit).all()
        
        logger.info(f"Fetched {len(contents)} content items")
        
        return AllContentResponse(
            success=True,
            total=total,
            data=[ContentResponse.from_orm(c) for c in contents]
        )
        
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch content"
        )


# Get single content endpoint
@app.get("/content/{content_id}", response_model=GenerateResponse)
async def get_content_by_id(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch a specific content by ID
    
    Args:
        content_id: Content ID
        db: Database session
        
    Returns:
        Specific content details
    """
    logger.info(f"Fetching content ID: {content_id}")
    
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        
        if not content:
            logger.warning(f"Content not found - ID: {content_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Content with ID {content_id} not found"
            )
        
        return GenerateResponse(
            success=True,
            message="Content retrieved successfully",
            data=ContentResponse.from_orm(content)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch content"
        )


# Delete content endpoint
@app.delete("/content/{content_id}")
async def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete content by ID
    
    Args:
        content_id: Content ID
        db: Database session
        
    Returns:
        Deletion status
    """
    logger.info(f"Deleting content ID: {content_id}")
    
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        
        if not content:
            logger.warning(f"Content not found - ID: {content_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Content with ID {content_id} not found"
            )
        
        db.delete(content)
        db.commit()
        
        logger.info(f"Content deleted successfully - ID: {content_id}")
        
        return {
            "success": True,
            "message": f"Content {content_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete content"
        )


# PHASE 3: AUTOMATION ENDPOINTS

# Keyword Clustering endpoint
@app.post("/keyword-clusters")
async def generate_keyword_clusters(request: ContentRequest):
    """
    Generate keyword clusters organized by search intent
    
    Args:
        request: ContentRequest with topic
        
    Returns:
        Keyword clusters grouped by intent
    """
    logger.info(f"Generating keyword clusters for: {request.topic}")
    
    try:
        if not ollama_client.is_available():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available"
            )
        
        clusters = KeywordService.generate_keyword_clusters(request.topic)
        
        return {
            "success": True,
            "topic": request.topic,
            "clusters": clusters
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating keyword clusters: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Bulk Content Generation endpoint
@app.post("/generate-bulk")
async def generate_bulk_content(
    request: ContentRequest,
    num_articles: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Generate multiple articles based on keyword clusters
    
    Args:
        request: ContentRequest with topic
        num_articles: Number of articles to generate (1-20)
        db: Database session
        
    Returns:
        List of generated articles
    """
    logger.info(f"Bulk generating {num_articles} articles for: {request.topic}")
    
    try:
        if not ollama_client.is_available():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available"
            )
        
        # Generate keyword clusters
        clusters = KeywordService.generate_keyword_clusters(request.topic)
        all_keywords = KeywordService.get_all_keywords(clusters)
        keywords_to_use = all_keywords[:num_articles]
        
        generated_articles = []
        errors = []
        
        for idx, keyword in enumerate(keywords_to_use, 1):
            try:
                logger.info(f"Generating article {idx}/{len(keywords_to_use)}: {keyword}")
                
                # Generate content
                content_result = ContentService.generate_content(keyword, db_session=db)
                
                if content_result.get("success"):
                    # Generate SEO metadata
                    seo_meta = ContentService.generate_title_and_description(
                        keyword,
                        content_result.get("content", "")[:200]
                    )
                    
                    # Calculate score
                    seo_score = SEOService.calculate_seo_score(
                        keyword,
                        seo_meta.get("title"),
                        content_result.get("content", ""),
                        seo_meta.get("description")
                    )
                    
                    # Save to database
                    db_content = Content(
                        topic=keyword,
                        title=content_result.get("title", keyword),
                        content=content_result.get("content", ""),
                        meta_title=seo_meta.get("title", ""),
                        meta_description=seo_meta.get("description", ""),
                        seo_score=seo_score
                    )
                    db.add(db_content)
                    db.commit()
                    db.refresh(db_content)
                    
                    # Add to vector DB for semantic linking
                    VectorService.add_document(
                        doc_id=f"article_{db_content.id}",
                        content=content_result.get("content", ""),
                        metadata={
                            "title": content_result.get("title", ""),
                            "topic": keyword,
                            "seo_score": seo_score
                        }
                    )
                    
                    generated_articles.append(ContentResponse.from_orm(db_content))
                else:
                    errors.append({"keyword": keyword, "error": "Generation failed"})
                    
            except Exception as e:
                logger.error(f"Error generating article for {keyword}: {str(e)}")
                errors.append({"keyword": keyword, "error": str(e)})
        
        return {
            "success": True,
            "topic": request.topic,
            "total_requested": num_articles,
            "total_generated": len(generated_articles),
            "articles": generated_articles,
            "errors": errors,
            "clusters": clusters
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Pipeline execution endpoint
@app.post("/pipeline")
async def run_seo_pipeline(
    request: ContentRequest,
    num_articles: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Run complete SEO automation pipeline
    
    Args:
        request: ContentRequest with topic
        num_articles: Number of articles to generate
        db: Database session
        
    Returns:
        Pipeline execution summary
    """
    logger.info(f"Running SEO pipeline for: {request.topic}")
    
    try:
        if not ollama_client.is_available():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available"
            )
        
        import asyncio
        pipeline_result = await PipelineService.run_pipeline(
            request.topic,
            num_articles=num_articles,
            include_vector_db=True
        )
        
        return {
            "success": True,
            "pipeline": pipeline_result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Vector DB Status endpoint
@app.get("/vector-db/status")
async def get_vector_db_status():
    """Get vector database statistics"""
    logger.info("Fetching vector DB status")
    
    try:
        stats = VectorService.get_collection_stats()
        return {
            "success": True,
            "vector_db": stats
        }
    except Exception as e:
        logger.error(f"Error getting vector DB status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API documentation"""
    return {
        "service": "KARS SEO Engine",
        "version": "2.0.0",
        "description": "AI-powered SEO automation system using local LLM",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "generate": "POST /generate",
            "keyword_clusters": "POST /keyword-clusters",
            "generate_bulk": "POST /generate-bulk",
            "pipeline": "POST /pipeline",
            "vector_db_status": "GET /vector-db/status",
            "get_all": "GET /content",
            "get_one": "GET /content/{id}",
            "delete": "DELETE /content/{id}"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "True") == "True"
    )
