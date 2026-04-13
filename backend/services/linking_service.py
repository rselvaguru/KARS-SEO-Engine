"""
Internal Linking Service
Finds related articles and generates internal link recommendations
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class LinkingService:
    """Service for managing internal links between articles"""
    
    @staticmethod
    def find_related_articles(
        current_topic: str,
        all_topics: List[str],
        max_links: int = 3
    ) -> List[Dict[str, str]]:
        """
        Find related articles based on keyword similarity
        
        Args:
            current_topic: Current article topic
            all_topics: List of all existing topics
            max_links: Maximum number of links to return
            
        Returns:
            List of related topics with their relevance score
        """
        if not all_topics or current_topic in all_topics:
            all_topics = [t for t in all_topics if t.lower() != current_topic.lower()]
        
        if not all_topics:
            return []
        
        logger.info(f"Finding related articles for: {current_topic}")
        
        # Split current topic into keywords
        current_keywords = set(current_topic.lower().split())
        
        # Score each topic
        related = []
        for topic in all_topics:
            topic_keywords = set(topic.lower().split())
            
            # Calculate overlap (Jaccard similarity)
            intersection = len(current_keywords & topic_keywords)
            
            if intersection > 0:
                relevance_score = intersection / max(len(current_keywords), len(topic_keywords))
                related.append({
                    "topic": topic,
                    "score": relevance_score
                })
        
        # Sort by score and return top N
        related.sort(key=lambda x: x["score"], reverse=True)
        return related[:max_links]
    
    @staticmethod
    def add_internal_links(
        content: str,
        related_articles: List[Dict[str, str]]
    ) -> str:
        """
        Append internal links section to content
        
        Args:
            content: Original content
            related_articles: List of related article dicts with 'topic' key
            
        Returns:
            Content with internal links appended
        """
        if not related_articles:
            return content
        
        logger.info(f"Adding {len(related_articles)} internal links to content")
        
        # Build links section
        links_section = "\n\n## Related Articles\n\n"
        links_section += "Learn more about related topics:\n\n"
        
        for idx, article in enumerate(related_articles, 1):
            topic = article.get("topic", "")
            if topic:
                links_section += f"- [{topic}](#{topic.lower().replace(' ', '-')})\n"
        
        return content + links_section
    
    @staticmethod
    def extract_topics_from_db(db_session, exclude_topic: str = None) -> List[str]:
        """
        Extract all topics from database
        
        Args:
            db_session: SQLAlchemy session
            exclude_topic: Topic to exclude (usually the current one)
            
        Returns:
            List of topics
        """
        from models.content_model import Content
        
        try:
            topics = db_session.query(Content.topic).distinct().all()
            topic_list = [t[0] for t in topics if t[0]]
            
            if exclude_topic:
                topic_list = [t for t in topic_list if t.lower() != exclude_topic.lower()]
            
            return topic_list
        except Exception as e:
            logger.error(f"Error extracting topics from database: {str(e)}")
            return []
