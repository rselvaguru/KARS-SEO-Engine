"""
Content Generation Service
Handles structured SEO content generation using Ollama with linking and optimization
"""

import logging
from ai.ollama_client import ollama_client
from utils.helpers import parse_structured_content, clean_text
from services.linking_service import LinkingService
from services.vector_service import VectorService

logger = logging.getLogger(__name__)


# Reusable System Prompt
SYSTEM_PROMPT = """You are an expert SEO content writer specializing in creating high-quality, engaging content.

Your content MUST have:
1. Clear, engaging introduction (2-3 sentences)
2. Strategic heading structure (H1 → H2 → H3)
3. Actionable insights and best practices
4. Bullet points for key takeaways
5. FAQ section with 4-5 questions
6. Conclusion with next steps

Requirements:
- Minimum 800 words
- No generic filler or repetition
- Include data-driven insights where possible
- Use markdown formatting properly
- Each H2 section: 150-200 words minimum
- Natural keyword integration (not forced)"""


class ContentService:
    """Service for generating SEO-optimized content"""
    
    @staticmethod
    def get_generation_prompt(topic: str, context: str = "") -> str:
        """
        Generate a structured prompt for content generation
        
        Args:
            topic: The topic to generate content for
            context: Optional additional context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Generate comprehensive, SEO-optimized content for the following topic:

TOPIC: "{topic}"
"""
        
        if context:
            prompt += f"CONTEXT: {context}\n\n"
        
        prompt += """STRUCTURE REQUIREMENTS:
1. H1 Title - Main topic headline
2. Introduction paragraph (100-150 words)
3. At least 4 H2 sections with detailed content
4. Include H3 subsections within H2 sections
5. Use bullet points and lists for clarity
6. FAQ section with Q&A format (minimum 4 questions)
7. Conclusion section

CONTENT GUIDELINES:
- Write for beginners and experts (accessible but detailed)
- Include actionable tips and best practices
- Add specific examples where relevant
- Maintain consistent tone and flow
- Total minimum 800 words
- Use engaging language, avoid jargon where possible
- Optimize for keywords naturally
- Include practical takeaways

OUTPUT FORMAT:
Use markdown formatting:
# H1 Title
## H2 Section
### H3 Subsection
- Bullet points for lists
Q: Question format for FAQ
A: Answer format for FAQ"""
        
        return prompt
    
    @staticmethod
    def generate_content(topic: str, db_session=None) -> dict:
        """
        Generate comprehensive SEO content for a topic with semantic internal linking
        
        Args:
            topic: The topic to generate content for
            db_session: SQLAlchemy session for fetching related articles
            
        Returns:
            Dictionary with generated content components
        """
        logger.info(f"Starting content generation pipeline for topic: {topic}")
        
        # Step 1: Generate main content
        user_prompt = ContentService.get_generation_prompt(topic)
        
        content_text = ollama_client.generate_text(user_prompt, SYSTEM_PROMPT)
        
        if not content_text:
            logger.error(f"Failed to generate content for topic: {topic}")
            return {
                "success": False,
                "error": "Failed to generate content. Ensure Ollama is running."
            }
        
        logger.info(f"✓ Content generated: {len(content_text)} characters")
        
        # Step 2: Add semantic internal links using vector DB
        try:
            # Try semantic linking first (vector DB)
            similar_docs = VectorService.get_similar(content_text, n=5, threshold=0.4)
            if similar_docs:
                semantic_links = [
                    {
                        "topic": doc.get("metadata", {}).get("topic", f"Article {doc['id']}"),
                        "score": doc["similarity"]
                    }
                    for doc in similar_docs[:3]
                ]
                content_text = LinkingService.add_internal_links(content_text, semantic_links)
                logger.info(f"✓ Added {len(semantic_links)} semantic internal links")
        except Exception as e:
            logger.debug(f"Semantic linking not available: {str(e)}")
        
        # Step 3: Fallback to keyword-based linking if database session provided
        if db_session and not similar_docs:
            try:
                related_articles = LinkingService.extract_topics_from_db(
                    db_session, 
                    exclude_topic=topic
                )
                
                if related_articles:
                    related_links = LinkingService.find_related_articles(
                        topic, 
                        related_articles, 
                        max_links=3
                    )
                    
                    if related_links:
                        content_text = LinkingService.add_internal_links(
                            content_text,
                            related_links
                        )
                        logger.info(f"✓ Added {len(related_links)} keyword-based internal links")
            except Exception as e:
                logger.warning(f"Could not add keyword-based links: {str(e)}")
        
        # Parse structured content
        parsed = parse_structured_content(content_text)
        
        logger.info(f"✓ Successfully generated content for topic: {topic}")
        
        return {
            "success": True,
            "title": parsed.get("h1", f"Complete Guide to {topic}"),
            "content": content_text,
            "structured": parsed
        }
    
    @staticmethod
    def generate_title_and_description(topic: str, content_preview: str = None) -> dict:
        """
        Generate SEO-optimized title and meta description
        
        Args:
            topic: The topic
            content_preview: First few lines of content for context
            
        Returns:
            Dictionary with optimized title and description
        """
        logger.info(f"Generating SEO title and description for: {topic}")
        
        system_prompt = """You are an SEO expert specializing in titles and meta descriptions.
Generate compelling, keyword-rich titles and descriptions that maximize CTR.

Requirements:
- Title: 50-60 characters, includes main keyword
- Description: 155-160 characters, compelling, includes main keyword
Format response as:
TITLE: [your title]
DESCRIPTION: [your description]"""
        
        prompt_text = f"""Generate optimized title and meta description for:
TOPIC: "{topic}"

Requirements:
- Title: 50-60 characters, must include "{topic}" keyword
- Description: 155-160 characters, persuasive, include keyword
- Both optimized for search engines and click-through rates"""
        
        if content_preview:
            prompt_text += f"\n\nContent Preview: {content_preview[:200]}"
        
        response = ollama_client.generate_text(prompt_text, system_prompt)
        
        if not response:
            logger.warning(f"Failed to generate SEO metadata for: {topic}")
            # Fallback
            return {
                "title": f"{topic} - Comprehensive Guide",
                "description": f"Learn everything about {topic}. Expert tips, best practices, and actionable insights."
            }
        
        # Parse response
        title = f"{topic} - Guide"
        description = f"Discover essential information about {topic}."
        
        for line in response.split("\n"):
            if "TITLE:" in line:
                title = line.replace("TITLE:", "").strip()
            elif "DESCRIPTION:" in line:
                description = line.replace("DESCRIPTION:", "").strip()
        
        return {
            "title": title[:60],
            "description": description[:160]
        }
