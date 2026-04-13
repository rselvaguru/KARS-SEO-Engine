"""
KARS SEO Engine - API Testing Guide

This guide provides curl commands to test all backend endpoints.
Make sure the backend is running on http://localhost:8000

Author: KARS SEO Engine Team
"""

# ====================================================
# 1. HEALTH CHECK
# ====================================================

# Check if backend and Ollama are running
curl -X GET http://localhost:8000/health

# Expected Response:
# {
#   "status": "healthy",
#   "service": "KARS SEO Engine",
#   "ollama": "available"
# }


# ====================================================
# 2. GENERATE SEO CONTENT
# ====================================================

# Generate content for a topic
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Machine Learning"}'

# Or with different topics:
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Digital Marketing Tips"}'

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Web Development with React"}'

# Expected Response (first 500 chars):
# {
#   "success": true,
#   "message": "Content generated successfully with SEO score: 82",
#   "data": {
#     "id": 1,
#     "topic": "Machine Learning",
#     "title": "Complete Guide to Machine Learning",
#     "content": "# Complete Guide to Machine Learning\n\n## What is Machine Learning?\n...",
#     "meta_title": "Machine Learning Guide - Essential Concepts & Tools",
#     "meta_description": "Learn machine learning fundamentals, algorithms ...",
#     "seo_score": 82,
#     "created_at": "2024-01-15T10:30:00"
#   }
# }


# ====================================================
# 3. GET ALL CONTENT
# ====================================================

# Fetch all generated content with pagination
curl -X GET "http://localhost:8000/content?skip=0&limit=10"

# Fetch with custom pagination
curl -X GET "http://localhost:8000/content?skip=10&limit=20"

# Expected Response:
# {
#   "success": true,
#   "total": 5,
#   "data": [
#     {
#       "id": 1,
#       "topic": "Machine Learning",
#       "title": "Complete Guide to Machine Learning",
#       "content": "...",
#       "meta_title": "...",
#       "meta_description": "...",
#       "seo_score": 82,
#       "created_at": "2024-01-15T10:30:00"
#     },
#     ...
#   ]
# }


# ====================================================
# 4. GET SINGLE CONTENT
# ====================================================

# Fetch specific content by ID
curl -X GET http://localhost:8000/content/1

# Expected Response:
# {
#   "success": true,
#   "message": "Content retrieved successfully",
#   "data": {
#     "id": 1,
#     "topic": "Machine Learning",
#     ...
#   }
# }


# ====================================================
# 5. DELETE CONTENT
# ====================================================

# Delete content by ID
curl -X DELETE http://localhost:8000/content/1

# Expected Response:
# {
#   "success": true,
#   "message": "Content 1 deleted successfully"
# }


# ====================================================
# ADVANCED: USING jq FOR PRETTY OUTPUT
# ====================================================

# Install jq first: brew install jq

# Pretty print health check
curl -s http://localhost:8000/health | jq .

# Generate and save response to file
curl -s -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python Programming"}' | jq . > response.json

# Extract just the content
curl -s -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python Programming"}' | jq '.data.content'

# Extract just the SEO score
curl -s -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python Programming"}' | jq '.data.seo_score'

# Get all topics
curl -s http://localhost:8000/content | jq '.data[].topic'


# ====================================================
# ADVANCED: BATCH GENERATION
# ====================================================

# Generate content for multiple topics
for topic in "SEO Tips" "Web Design" "Content Marketing" "Social Media"; do
  echo "Generating content for: $topic"
  curl -s -X POST http://localhost:8000/generate \
    -H "Content-Type: application/json" \
    -d "{\"topic\": \"$topic\"}" | jq '.data.seo_score'
  sleep 2  # 2 second delay between requests
done


# ====================================================
# ERROR HANDLING
# ====================================================

# Invalid topic (too short)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI"}'

# Response:
# {
#   "detail": [
#     {
#       "type": "string_too_short",
#       "loc": ["body", "topic"],
#       "msg": "String should have at least 3 characters",
#       "input": "AI"
#     }
#   ]
# }

# Content not found
curl -X GET http://localhost:8000/content/999

# Response:
# {
#   "success": false,
#   "message": "Not Found",
#   "error": "Content with ID 999 not found"
# }

# Ollama not available
# Response when Ollama is not running:
# {
#   "detail": "Ollama service is not available. Please ensure Ollama is running."
# }


# ====================================================
# PERFORMANCE TESTING
# ====================================================

# Time how long content generation takes
time curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence"}'

# Load test with Apache Bench (install: brew install httpd)
ab -n 10 -c 1 http://localhost:8000/health

# More advanced testing with siege
# brew install siege
# siege -c 5 -r 2 http://localhost:8000/health


# ====================================================
# TESTING WITH PYTHON REQUESTS
# ====================================================

"""
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Generate content
response = requests.post(
    'http://localhost:8000/generate',
    json={'topic': 'Machine Learning'}
)
content = response.json()
print(f"SEO Score: {content['data']['seo_score']}")
print(f"Title: {content['data']['meta_title']}")

# Get all content
response = requests.get('http://localhost:8000/content?skip=0&limit=5')
contents = response.json()
print(f"Total content items: {contents['total']}")

# Delete content
response = requests.delete('http://localhost:8000/content/1')
print(response.json())
"""

# ====================================================
# NOTES
# ====================================================

# 1. First content generation takes 30-60 seconds (model loading)
# 2. Subsequent generations are faster (10-30 seconds)
# 3. Content quality depends on topic specificity
# 4. SEO score is calculated based on multiple factors (0-100)
# 5. All timestamps are in UTC format

# ====================================================
# DOCUMENTATION
# ====================================================

# Interactive API documentation:
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# View OpenAPI schema:
# curl http://localhost:8000/openapi.json
