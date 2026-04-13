"""
Utility helper functions
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def parse_structured_content(text: str) -> dict:
    """
    Parse AI-generated content into structured format
    Handles various formatting styles
    
    Args:
        text: Raw AI output text
        
    Returns:
        Dictionary with parsed content sections
    """
    result = {
        "title": "",
        "h1": "",
        "h2_sections": [],
        "h3_sections": [],
        "paragraphs": [],
        "faqs": []
    }
    
    lines = text.split("\n")
    current_h2 = None
    current_h3 = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
            
        # Parse H1
        if line.startswith("# "):
            result["h1"] = line.replace("# ", "").strip()
        
        # Parse H2
        elif line.startswith("## "):
            current_h2 = line.replace("## ", "").strip()
            result["h2_sections"].append({"heading": current_h2, "content": ""})
        
        # Parse H3
        elif line.startswith("### "):
            current_h3 = line.replace("### ", "").strip()
            if current_h2:
                result["h3_sections"].append({"parent": current_h2, "heading": current_h3, "content": ""})
        
        # Parse FAQ
        elif line.startswith("Q:") or line.startswith("Question:"):
            faq_q = line.replace("Q:", "").replace("Question:", "").strip()
            result["faqs"].append({"question": faq_q, "answer": ""})
        
        elif (line.startswith("A:") or line.startswith("Answer:")) and result["faqs"]:
            faq_a = line.replace("A:", "").replace("Answer:", "").strip()
            result["faqs"][-1]["answer"] = faq_a
        
        # Regular paragraph content
        elif current_h2 or current_h3:
            if result["h3_sections"]:
                result["h3_sections"][-1]["content"] += line + " "
            elif result["h2_sections"]:
                result["h2_sections"][-1]["content"] += line + " "
    
    return result


def clean_text(text: str) -> str:
    """Remove extra whitespace and clean text"""
    return " ".join(text.split())


def generate_seo_keyword_list(topic: str, count: int = 5) -> list:
    """Generate basic keyword variations from topic"""
    keywords = [topic.lower()]
    
    # Add simple variations
    if len(topic.split()) > 1:
        keywords.append(topic.split()[0].lower())
    
    keywords.extend([
        f"best {topic.lower()}",
        f"{topic.lower()} guide",
        f"{topic.lower()} tips",
    ])
    
    return keywords[:count]


def log_generation(topic: str, model: str, tokens: int = 0):
    """Log content generation for tracking"""
    logger.info(
        f"Content generated - Topic: {topic}, Model: {model}, "
        f"Timestamp: {datetime.utcnow().isoformat()}"
    )


def truncate_text(text: str, max_length: int = 160) -> str:
    """Truncate text to max length, ending at word boundary"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(" ")
    
    if last_space > max_length * 0.8:  # If last space is reasonably close
        return truncated[:last_space] + "..."
    
    return truncated + "..."
