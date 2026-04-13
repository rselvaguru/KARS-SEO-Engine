"""
SEO Optimization Service
Calculates SEO scores and provides optimization recommendations
"""

import logging
import re

logger = logging.getLogger(__name__)


class SEOService:
    """Service for SEO analysis and scoring"""
    
    @staticmethod
    def calculate_seo_score(
        topic: str,
        title: str,
        content: str,
        meta_description: str
    ) -> int:
        """
        Calculate SEO score based on 5 major factors
        Score range: 0-100
        
        Args:
            topic: The target topic/keyword
            title: Content title
            content: Full content text
            meta_description: Meta description
            
        Returns:
            SEO score (0-100)
        """
        score = 0
        topic_lower = topic.lower()
        
        logger.info(f"Calculating SEO score for topic: {topic}")
        
        # 1. HEADINGS (20 points) - Structure quality
        h1_count = len(re.findall(r"^#\s+", content, re.MULTILINE))
        h2_count = len(re.findall(r"^##\s+", content, re.MULTILINE))
        h3_count = len(re.findall(r"^###\s+", content, re.MULTILINE))
        heading_score = 0
        
        if h1_count >= 1:
            heading_score += 5
        if h2_count >= 2:
            heading_score += 8
        if h3_count >= 2:
            heading_score += 7
        
        score += min(heading_score, 20)
        
        # 2. CONTENT LENGTH (20 points) - Depth & authority
        word_count = len(content.split())
        if word_count >= 1000:
            score += 20
        elif word_count >= 800:
            score += 18
        elif word_count >= 600:
            score += 14
        elif word_count >= 400:
            score += 10
        elif word_count >= 200:
            score += 5
        
        # 3. FAQ SECTION (20 points) - User engagement signal
        if "FAQ" in content or ("Q:" in content and "A:" in content):
            score += 20
        
        # 4. KEYWORD IN TITLE (20 points) - Primary signal
        if topic_lower in title.lower():
            score += 15
        if 50 <= len(title) <= 60:
            score += 5
        
        # 5. META DESCRIPTION (20 points) - Click-through optimization
        if topic_lower in meta_description.lower():
            score += 10
        if 155 <= len(meta_description) <= 160:
            score += 10
        elif 150 <= len(meta_description) <= 165:
            score += 5
        
        # Cap score at 100
        score = min(score, 100)
        
        logger.info(f"SEO Score calculated: {score}/100 for topic: {topic} (Length: {word_count}w, Headings: {h1_count}H1/{h2_count}H2/{h3_count}H3)")
        
        return score
    
    @staticmethod
    def get_seo_recommendations(
        topic: str,
        title: str,
        content: str,
        meta_description: str,
        score: int
    ) -> list:
        """
        Generate SEO optimization recommendations
        
        Args:
            topic: The target topic/keyword
            title: Content title
            content: Full content text
            meta_description: Meta description
            score: Current SEO score
            
        Returns:
            List of recommendations
        """
        recommendations = []
        topic_lower = topic.lower()
        
        # Title recommendations
        if topic_lower not in title.lower():
            recommendations.append("Add the main keyword to the title")
        if len(title) < 50:
            recommendations.append("Extend title to at least 50 characters")
        if len(title) > 60:
            recommendations.append("Reduce title to under 60 characters")
        
        # Meta description recommendations
        if len(meta_description) < 155:
            recommendations.append("Extend meta description to at least 155 characters")
        if len(meta_description) > 160:
            recommendations.append("Reduce meta description to under 160 characters")
        if topic_lower not in meta_description.lower():
            recommendations.append("Include main keyword in meta description")
        
        # Content structure
        if len(re.findall(r"^##\s+", content, re.MULTILINE)) < 2:
            recommendations.append("Add at least 2 H2 subheadings")
        if len(re.findall(r"^###\s+", content, re.MULTILINE)) < 2:
            recommendations.append("Add H3 subheadings for better structure")
        if len(content.split()) < 400:
            recommendations.append("Expand content to at least 400 words")
        
        # Keyword usage
        keyword_count = content.lower().count(topic_lower)
        if keyword_count < 3:
            recommendations.append("Increase keyword mentions (natural placement)")
        
        # General
        if score < 60:
            recommendations.append("Comprehensive improvements needed for better SEO")
        
        return recommendations[:5]  # Return top 5 recommendations
