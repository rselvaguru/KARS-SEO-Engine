"""
Pipeline Service - Automation Engine
Orchestrates keyword clustering, bulk content generation, semantic linking
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from services.keyword_service import KeywordService
from services.content_service import ContentService
from services.vector_service import VectorService
from db.database import SessionLocal
from models.content_model import Content

logger = logging.getLogger(__name__)


class PipelineService:
    """Orchestrates the complete SEO content generation pipeline"""

    @staticmethod
    async def run_pipeline(
        topic: str,
        num_articles: int = 5,
        include_vector_db: bool = True
    ) -> Dict:
        """
        Run complete SEO pipeline for a topic
        
        Args:
            topic: Main topic to generate content for
            num_articles: Number of articles to generate (1-20)
            include_vector_db: Whether to add to vector DB
        
        Returns:
            Pipeline execution summary with results
        """
        logger.info(f"Starting SEO pipeline for topic: {topic}")
        
        try:
            db = SessionLocal()
            results = {
                "topic": topic,
                "started_at": datetime.now().isoformat(),
                "status": "in_progress",
                "steps": {
                    "keyword_clustering": None,
                    "content_generation": [],
                    "vector_indexing": None
                },
                "stats": {
                    "total_articles": 0,
                    "total_keywords": 0,
                    "vector_db_count": 0,
                    "errors": []
                }
            }
            
            # Step 1: Generate keyword clusters
            logger.info("Step 1: Generating keyword clusters...")
            clusters = KeywordService.generate_keyword_clusters(topic)
            results["steps"]["keyword_clustering"] = clusters
            
            all_keywords = KeywordService.get_all_keywords(clusters)
            results["stats"]["total_keywords"] = len(all_keywords)
            logger.info(f"Generated {len(all_keywords)} keywords in 3 clusters")
            
            # Step 2: Generate content for keywords
            logger.info(f"Step 2: Generating content for {num_articles} keywords...")
            keywords_to_use = all_keywords[:num_articles]
            
            for idx, keyword in enumerate(keywords_to_use, 1):
                try:
                    logger.info(f"Generating article {idx}/{num_articles}: {keyword}")
                    
                    # Generate content using existing service
                    content_data = ContentService.generate_content(
                        topic=keyword,
                        db_session=db
                    )
                    
                    # Store in database
                    db_content = Content(
                        topic=keyword,
                        title=content_data.get("title", ""),
                        content=content_data.get("content", ""),
                        meta_title=content_data.get("meta_title", ""),
                        meta_description=content_data.get("meta_description", ""),
                        seo_score=content_data.get("seo_score", 0)
                    )
                    db.add(db_content)
                    db.commit()
                    
                    # Step 3: Add to vector DB
                    if include_vector_db:
                        VectorService.add_document(
                            doc_id=f"article_{db_content.id}",
                            content=content_data.get("content", ""),
                            metadata={
                                "title": content_data.get("title", ""),
                                "topic": keyword,
                                "seo_score": content_data.get("seo_score", 0)
                            }
                        )
                    
                    results["steps"]["content_generation"].append({
                        "keyword": keyword,
                        "article_id": db_content.id,
                        "title": content_data.get("title", ""),
                        "seo_score": content_data.get("seo_score", 0),
                        "status": "success"
                    })
                    
                    results["stats"]["total_articles"] += 1
                    
                except Exception as e:
                    logger.error(f"Error generating article for {keyword}: {e}")
                    results["stats"]["errors"].append({
                        "keyword": keyword,
                        "error": str(e)
                    })
            
            # Get vector DB stats
            if include_vector_db:
                vector_stats = VectorService.get_collection_stats()
                results["steps"]["vector_indexing"] = vector_stats
                results["stats"]["vector_db_count"] = vector_stats.get("documents", 0)
            
            # Finalize
            results["status"] = "completed"
            results["completed_at"] = datetime.now().isoformat()
            
            logger.info(f"Pipeline completed: {results['stats']['total_articles']} articles generated")
            db.close()
            
            return results
        
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            return {
                "topic": topic,
                "status": "error",
                "error": str(e)
            }

    @staticmethod
    def get_pipeline_status() -> Dict:
        """Get status of vector DB and system"""
        return {
            "vector_db": VectorService.get_collection_stats(),
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def bulk_generate(
        keywords: List[str],
        include_vector_db: bool = True
    ) -> Dict:
        """
        Generate content for multiple keywords
        
        Args:
            keywords: List of keywords to generate content for
            include_vector_db: Whether to add to vector DB
        
        Returns:
            Generation results
        """
        logger.info(f"Bulk generating content for {len(keywords)} keywords")
        
        try:
            db = SessionLocal()
            results = {
                "keywords": keywords,
                "generated": [],
                "errors": []
            }
            
            for keyword in keywords:
                try:
                    content_data = ContentService.generate_content(
                        topic=keyword,
                        db_session=db
                    )
                    
                    db_content = Content(
                        topic=keyword,
                        title=content_data.get("title", ""),
                        content=content_data.get("content", ""),
                        meta_title=content_data.get("meta_title", ""),
                        meta_description=content_data.get("meta_description", ""),
                        seo_score=content_data.get("seo_score", 0)
                    )
                    db.add(db_content)
                    db.commit()
                    
                    if include_vector_db:
                        VectorService.add_document(
                            doc_id=f"article_{db_content.id}",
                            content=content_data.get("content", ""),
                            metadata={"title": content_data.get("title", ""), "topic": keyword}
                        )
                    
                    results["generated"].append({
                        "keyword": keyword,
                        "article_id": db_content.id,
                        "seo_score": content_data.get("seo_score", 0)
                    })
                
                except Exception as e:
                    logger.error(f"Error generating {keyword}: {e}")
                    results["errors"].append({"keyword": keyword, "error": str(e)})
            
            db.close()
            return results
        
        except Exception as e:
            logger.error(f"Bulk generation error: {e}")
            return {"status": "error", "error": str(e)}
