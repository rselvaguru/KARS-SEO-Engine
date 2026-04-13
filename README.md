# KARS SEO Engine - AI-Powered SEO Automation Platform

A production-ready MVP platform for AI-powered SEO content generation using a local LLM. Generate, optimize, and manage SEO content with minimal latency and zero external API dependencies.

## 🎯 Overview

**KARS SEO Engine** is a complete, modern SaaS-ready platform that combines:
- **FastAPI Backend** - High-performance Python REST API
- **Next.js Frontend** - Modern React with TypeScript
- **Ollama LLM** - Local, privacy-respecting AI
- **SQLite Database** - Lightweight, portable data storage

Generate SEO-optimized content for any topic in seconds, including titles, headings, FAQs, and SEO metadata.

---

## ⚙️ Technology Stack

### Backend
- **Python 3.10+** - Core language
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **Ollama** - Local LLM inference engine (phi model)

### Frontend
- **Next.js 14** - React framework with TypeScript
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript

### Database
- **SQLite** - Zero-configuration SQL database

### Environment
- **macOS** (Apple Silicon M1 compatible)
- **VS Code** - Editor

---

## 📋 Core Features

### MVP Features
1. **Topic Input** - User enters any topic/keyword
2. **AI Content Generation** - Generates SEO-optimized content:
   - Professional SEO title
   - H1, H2, H3 structured headings
   - Rich paragraph content
   - FAQ section
3. **SEO Optimization**:
   - Meta title (50-60 chars)
   - Meta description (155-160 chars)
4. **Content Storage** - Save all generated content to database
5. **Content Retrieval** - View, search, and manage all generated content
6. **SEO Scoring** - Rule-based scoring system (0-100):
   - Title optimization (20 points)
   - Meta description (15 points)
   - Content structure (15 points)
   - Keyword usage (15 points)
   - Content length (15 points)
   - Readability (15 points)

### Bonus Features
- **Copy-to-Clipboard** - Quickly copy content for use elsewhere
- **Delete Content** - Manage and clean up old content
- **Backend Health Monitoring** - Real-time status indicator
- **Responsive UI** - Works on desktop, tablet, mobile
- **Error Handling** - Comprehensive error messages and recovery

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+**
   ```bash
   python3 --version  # Should be 3.10 or higher
   ```

2. **Node.js 18+**
   ```bash
   node --version  # Should be 18 or higher
   npm --version
   ```

3. **Ollama** - Local AI inference engine
   - Install from: https://ollama.ai
   - Or via Homebrew: `brew install ollama`

---

## 📥 Installation & Setup

### Step 1: Clone/Open Project

Navigate to the project directory:
```bash
cd "/Users/selvagurunathanramalingam/2026/github/KARS SEO Engine"
```

### Step 2: Set Up Ollama (Local AI)

#### Option A: Install Ollama (Recommended)

**macOS Installation:**

1. **Download & Install Ollama**
   ```bash
   # Via Homebrew
   brew install ollama
   
   # Or download from https://ollama.ai
   ```

2. **Start Ollama Service**
   ```bash
   # Start in background
   ollama serve
   
   # Or as macOS service
   brew services start ollama
   ```

3. **Download phi Model**
   ```bash
   ollama pull phi
   ```

   This downloads the phi-2 model (~2.7GB). First time only - takes 40-60 seconds.

4. **Verify Ollama is Running**
   ```bash
   curl http://localhost:11434/api/tags
   
   # Should return a JSON with available models
   ```

#### Option B: Use Existing Ollama Installation

If Ollama is already installed:
```bash
# Make sure it's running
ollama serve &

# Pull phi model (if not already pulled)
ollama pull phi
```

---

### Step 3: Set Up Backend (FastAPI)

1. **Create Python Virtual Environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or: venv\Scripts\activate  # On Windows
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Verify .env Configuration**
   ```bash
   cat .env  # Check environment variables
   ```

   Default `.env` values:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=phi
   DATABASE_URL=sqlite:///./kars_seo.db
   DEBUG=True
   LOG_LEVEL=INFO
   ```

4. **Start FastAPI Backend**
   ```bash
   # With auto-reload (development)
   python main.py
   
   # Or with uvicorn directly
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Expected Output:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete
   INFO:     ✓ Ollama is available (Model: phi)
   ```

5. **Verify Backend**
   - Health Check: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

### Step 4: Set Up Frontend (Next.js)

1. **Install Node Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment** (Optional)
   
   Create `.env.local` if backend is on different URL:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start Next.js Development Server**
   ```bash
   npm run dev
   ```

   **Expected Output:**
   ```
   ▲ Next.js 14.0.0
   - Local:        http://localhost:3000
   ```

4. **Open in Browser**
   ```
   http://localhost:3000
   ```

---

## 🎮 Usage Guide

### 1. Generate SEO Content

1. **Open Frontend**: http://localhost:3000
2. **Enter Topic**: Type any topic (e.g., "Machine Learning", "Digital Marketing")
3. **Click Generate**: Wait for AI to generate content (10-30 seconds)
4. **View Results**:
   - SEO Title & Meta Description
   - Full structured content
   - SEO Score (0-100)
   - FAQ section

### 2. Copy & Use Content

- **Copy Individual Fields**: Click 📋 icon next to Meta Title/Description
- **Copy All Content**: Click "📋 Copy Content" button

### 3. Manage Content

- **View All**: Click "View Generated Content" on home page
- **Delete**: Click "🗑️ Delete" button on any card
- **Search**: List shows all previously generated content

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Generate Content
```
POST /generate
Content-Type: application/json

Request:
{
  "topic": "Machine Learning"
}

Response:
{
  "success": true,
  "message": "Content generated successfully with SEO score: 82",
  "data": {
    "id": 1,
    "topic": "Machine Learning",
    "title": "Complete Guide to Machine Learning",
    "content": "...",
    "meta_title": "Machine Learning Guide - Essential Concepts & Tools",
    "meta_description": "Learn machine learning fundamentals, algorithms, and best practices with this comprehensive guide.",
    "seo_score": 82,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### 2. Get All Content
```
GET /content?skip=0&limit=10

Response:
{
  "success": true,
  "total": 5,
  "data": [...]
}
```

#### 3. Get Single Content
```
GET /content/{id}

Response:
{
  "success": true,
  "message": "Content retrieved successfully",
  "data": {...}
}
```

#### 4. Delete Content
```
DELETE /content/{id}

Response:
{
  "success": true,
  "message": "Content 1 deleted successfully"
}
```

#### 5. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "KARS SEO Engine",
  "ollama": "available"
}
```

---

## 🗂️ Project Structure

```
KARS SEO Engine/
│
├── backend/
│   ├── main.py                   # FastAPI app entry point
│   ├── .env                      # Environment configuration
│   ├── ai/
│   │   └── ollama_client.py     # Ollama API integration
│   ├── services/
│   │   ├── content_service.py   # Content generation logic
│   │   └── seo_service.py       # SEO optimization & scoring
│   ├── db/
│   │   └── database.py          # SQLAlchemy setup
│   ├── models/
│   │   └── content_model.py     # SQLAlchemy models
│   ├── schemas/
│   │   └── content_schema.py    # Pydantic validation schemas
│   └── utils/
│       └── helpers.py            # Utility functions
│
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx             # Main app component
│   │   └── index.tsx            # Home page
│   ├── components/
│   │   ├── TopicForm.tsx        # Input form component
│   │   └── ContentCard.tsx      # Content display component
│   ├── services/
│   │   └── api.ts              # API client
│   ├── styles/
│   │   └── globals.css         # Global styles
│   ├── package.json            # NPM dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── next.config.js          # Next.js config
│   ├── tailwind.config.js      # Tailwind CSS config
│   └── postcss.config.js       # PostCSS config
│
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

---

## 🌍 Environment Variables

### Backend (.env)
```
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi

# Database
DATABASE_URL=sqlite:///./kars_seo.db

# FastAPI
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔧 Development

### Adding New Features

1. **Backend Service**
   - Add logic in `backend/services/*.py`
   - Add endpoint in `backend/main.py`
   - Update `schemas/content_schema.py` if needed

2. **Frontend Component**
   - Create component in `frontend/components/`
   - Import in `frontend/pages/_app.tsx`
   - Use API client from `frontend/services/api.ts`

### Database Migrations

Schema changes:
```python
# Edit backend/models/content_model.py
# Restart backend server
```

---

## 📊 SEO Score Calculation

Score Range: 0-100

| Factor | Weight | Criteria |
|--------|--------|----------|
| Title | 20% | Keyword presence, length (50-60 chars) |
| Meta Description | 15% | Keyword presence, length (155-160 chars) |
| Structure | 15% | H2/H3 headings, FAQ section |
| Keywords | 15% | Keyword frequency, density (0.5-3%) |
| Length | 15% | Minimum 400+ words |
| Readability | 20% | Paragraphs, formatting, length |

**Score Interpretation:**
- **80-100**: Excellent SEO
- **60-79**: Good SEO
- **0-59**: Needs Improvement

---

## 🐛 Troubleshooting

### Problem: Backend won't start
```
Error: Cannot connect to Ollama
```

**Solution:**
1. Ensure Ollama is running: `ollama serve`
2. Verify port 11434 is not in use
3. Check Ollama is accessible: `curl http://localhost:11434/api/tags`

### Problem: Frontend can't connect to backend
```
Cannot connect to backend. Ensure backend is running on http://localhost:8000
```

**Solution:**
1. Backend must be running: `python main.py`
2. Check port 8000 is available
3. Verify CORS is enabled (it is by default)

### Problem: Slow content generation
```
Content generation takes >1 minute
```

**Reasons:**
- First generation downloads phi model (~2.7GB)
- phi language model is designed for M1 chips but can run on any system
- System RAM needs ~4GB free

**Solutions:**
- Allow first generation to complete fully
- Close other applications to free up RAM
- Use a machine with 8GB+ RAM for faster generation

### Problem: Content quality is poor
```
Generated content is low quality or repetitive
```

**Solutions:**
1. Use more specific topics (e.g., "React.js hooks" vs "JavaScript")
2. Longer topics generate better content
3. Try different phrasings of the topic
4. Ensure Ollama phi model is latest: `ollama pull phi`

---

## 📈 Performance Optimization

### Backend
- Async processing with FastAPI
- Connection pooling with SQLAlchemy
- Efficient SQLite queries with indexing

### Frontend
- Code splitting with Next.js
- Tailwind CSS optimization
- Component lazy loading

### Database
- SQLite with indexes on frequently queried columns
- Query pagination (default 10 items)

---

## 🔐 Security Considerations

### Production Deployment
1. **Environment Variables**: Use secure .env management
2. **API Keys**: Store sensitive data securely
3. **CORS**: Restrict to trusted domains
4. **Rate Limiting**: Implement request throttling
5. **Authentication**: Add user auth layer
6. **HTTPS**: Use SSL/TLS in production

### Current Limitations
- No user authentication (add OAuth/JWT for production)
- CORS allows all origins (restrict in production)
- Debug mode enabled (disable for production)

---

## 📦 Deployment

### Local Development
Already set up! Just run:
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Docker Deployment (Optional)

Create `Dockerfile` for containerization:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Deployment

For production (AWS, Vercel, Heroku):
1. **Backend**: Use gunicorn + Nginx reverse proxy
2. **Frontend**: Deploy to Vercel or AWS
3. **Database**: Migrate to PostgreSQL
4. **LLM**: Consider hosted inference endpoint for scalability

---

## 🤝 Contributing

This is a foundation for further development. Future enhancements:

- [ ] Multi-language support (English, Tamil, Spanish)
- [ ] Advanced SEO recommendations
- [ ] Content regeneration
- [ ] Batch content generation
- [ ] User authentication & teams
- [ ] API rate limiting
- [ ] Content scheduling
- [ ] Analytics dashboard
- [ ] A/B testing framework
- [ ] Bulk import/export

---

## 📝 License

This project is provided as-is for educational and commercial use.

---

## 🆘 Support & Documentation

### Quick Links
- **FastAPI Docs**: http://localhost:8000/docs (when backend running)
- **Next.js Docs**: https://nextjs.org/docs
- **Ollama Docs**: https://github.com/ollama/ollama
- **Tailwind CSS**: https://tailwindcss.com/docs

### Useful Commands

**Backend**
```bash
# Start with auto-reload
python main.py

# Run with gunicorn (production)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Check logs
tail -f backend.log
```

**Frontend**
```bash
# Development with hot reload
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

**Database**
```bash
# Access SQLite
sqlite3 kars_seo.db

# View tables
sqlite3 kars_seo.db ".tables"

# Delete database to start fresh
rm kars_seo.db  # Backend will recreate on startup
```

---

## 🎯 Next Steps

1. **Verify Installation**
   - Run health check: `curl http://localhost:8000/health`
   - Open frontend: http://localhost:3000

2. **Generate First Content**
   - Enter topic: "Digital Marketing"
   - Watch AI generate content in real-time

3. **Explore Features**
   - Copy generated content
   - View SEO score breakdown
   - Try different topics

4. **Extend Platform**
   - Add user authentication
   - Integrate with search engines
   - Create analytics dashboard
   - Build content approval workflow

---

## 📞 Questions?

Refer to individual component documentation:
- Backend API: Check FastAPI Swagger UI at http://localhost:8000/docs
- Frontend: Review component props in TypeScript files
- Ollama: Visit https://ollama.ai for model details

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production Ready ✅

---

Happy content generation! 🚀
