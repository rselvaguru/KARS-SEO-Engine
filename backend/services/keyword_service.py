"""
Keyword Service - Semantic Keyword Clustering
Generates keyword clusters using Ollama for information architecture
"""

import json
import logging
from typing import List, Dict
from ai.ollama_client import ollama_client

logger = logging.getLogger(__name__)


class KeywordService:
    """Generates and clusters keywords for content strategy"""

    CLUSTERING_PROMPT = """You are an expert SEO strategist. Given a topic, generate relevant keywords and organize them by intent.

Generate exactly 30-40 unique keywords for the topic: {topic}

Classify each keyword into these three categories:
1. INFORMATIONAL - Keywords for "how-to", educational, research (searches wanting to learn)
2. TRANSACTIONAL - Keywords for "buying", "pricing", "services" (searches wanting to buy/act)
3. NAVIGATIONAL - Keywords for brand/product names, specific tool names

Return a valid JSON object (NO markdown, NO code blocks) with this EXACT structure:
{{
  "topic": "{topic}",
  "informational_keywords": ["keyword1", "keyword2", ...],
  "transactional_keywords": ["keyword1", "keyword2", ...],
  "navigational_keywords": ["keyword1", "keyword2", ...]
}}

IMPORTANT RULES:
- Do NOT include markdown formatting
- Do NOT use code blocks
- Return ONLY valid JSON
- Each array should have 8-15 keywords
- Keywords must be unique and relevant"""

    @staticmethod
    def generate_keyword_clusters(topic: str) -> Dict:
        """
        Generate keyword clusters for a topic
        
        Args:
            topic: Main topic/keyword
        
        Returns:
            Dict with organized keyword clusters
        """
        try:
            logger.info(f"Generating keyword clusters for: {topic}")
            
            # Create system and user prompts
            system_prompt = "You are an expert SEO strategist. Generate SEO keywords and structure them by search intent."
            user_prompt = KeywordService.CLUSTERING_PROMPT.format(topic=topic)
            
            # Call Ollama to generate keywords
            response = ollama_client.generate_text(user_prompt, system_prompt)
            
            # Parse JSON response
            parsed = KeywordService._parse_keyword_response(response)
            
            if parsed:
                logger.info(f"Successfully generated clusters with {sum(len(v) for k, v in parsed.items() if k != 'topic')} keywords")
                return parsed
            else:
                logger.warning("Failed to parse keyword response, returning fallback")
                return KeywordService._generate_fallback_clusters(topic)
        
        except Exception as e:
            logger.error(f"Error generating keyword clusters: {e}")
            return KeywordService._generate_fallback_clusters(topic)

    @staticmethod
    def _parse_keyword_response(response: str) -> Dict:
        """
        Parse JSON response from Ollama
        
        Args:
            response: Raw text response from Ollama
        
        Returns:
            Parsed keyword clusters dict or None
        """
        try:
            # Remove markdown formatting if present
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()
            
            # Try to parse JSON
            data = json.loads(response)
            
            # Validate structure
            if all(key in data for key in ["topic", "informational_keywords", "transactional_keywords", "navigational_keywords"]):
                return data
            
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return None

    @staticmethod
    def _generate_fallback_clusters(topic: str) -> Dict:
        """
        Generate fallback keyword clusters when Ollama fails
        
        Args:
            topic: Main topic
        
        Returns:
            Basic keyword structure
        """
        words = topic.lower().split()
        main_word = words[0]
        
        return {
            "topic": topic,
            "informational_keywords": [
                f"how to {topic}",
                f"{topic} guide",
                f"{topic} tips",
                f"{main_word} best practices",
                f"{topic} tutorial",
                f"{topic} benefits",
                f"{topic} explained",
                f"{main_word} for beginners"
            ],
            "transactional_keywords": [
                f"{topic} service",
                f"buy {topic}",
                f"{topic} pricing",
                f"get started with {topic}",
                f"{topic} software",
                f"{topic} platform",
                f"{topic} tools",
                f"best {topic} service"
            ],
            "navigational_keywords": [
                topic,
                f"{topic} official",
                f"{main_word} website",
                f"{main_word} app",
                f"{main_word} platform"
            ]
        }

    @staticmethod
    def get_all_keywords(clusters: Dict) -> List[str]:
        """Get flat list of all keywords from clusters"""
        keywords = []
        for key in ["informational_keywords", "transactional_keywords", "navigational_keywords"]:
            keywords.extend(clusters.get(key, []))
        return keywords

    @staticmethod
    def get_keywords_by_intent(clusters: Dict, intent: str) -> List[str]:
        """
        Get keywords filtered by intent
        
        Args:
            clusters: Keyword clusters dict
            intent: One of 'informational', 'transactional', 'navigational'
        
        Returns:
            List of keywords for that intent
        """
        key = f"{intent}_keywords"
        return clusters.get(key, [])
