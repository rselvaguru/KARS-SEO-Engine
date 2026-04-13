#!/bin/bash

# KARS SEO Engine - Complete Setup & Run Guide
# Fast reference for all setup and execution commands

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   KARS SEO Engine - Quick Command Reference                ║"
echo "║   AI-Powered SEO Content Generation Platform              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# SECTION 1: OLLAMA SETUP (One-time)
# ============================================================

echo "┌─ OLLAMA SETUP ─────────────────────────────────────────────┐"
echo "│"
echo "│ 1. Install Ollama (macOS):"
echo "│    $ brew install ollama"
echo "│"
echo "│ 2. Download phi model (first time only, ~2.7GB):"
echo "│    $ ollama pull phi"
echo "│"
echo "│ 3. Start Ollama service:"
echo "│    $ ollama serve"
echo "│"
echo "│ 4. Verify installation:"
echo "│    $ curl http://localhost:11434/api/tags"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 2: BACKEND SETUP (First time)
# ============================================================

echo "┌─ BACKEND SETUP (First Time) ──────────────────────────────┐"
echo "│"
echo "│ $ cd backend"
echo "│ $ python3 -m venv venv"
echo "│ $ source venv/bin/activate"
echo "│ $ pip install -r ../requirements.txt"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 3: BACKEND RUN (Every time)
# ============================================================

echo "┌─ BACKEND RUN (Every Time) ────────────────────────────────┐"
echo "│"
echo "│ Step 1: Navigate to backend"
echo "│    $ cd backend"
echo "│"
echo "│ Step 2: Activate virtual environment"
echo "│    $ source venv/bin/activate"
echo "│"
echo "│ Step 3: Start FastAPI server"
echo "│    $ python main.py"
echo "│"
echo "│    Expected output:"
echo "│    > Uvicorn running on http://0.0.0.0:8000"
echo "│    > ✓ Ollama is available (Model: phi)"
echo "│"
echo "│    API accessible at:"
echo "│    • Swagger UI: http://localhost:8000/docs"
echo "│    • ReDoc: http://localhost:8000/redoc"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 4: FRONTEND SETUP (First time)
# ============================================================

echo "┌─ FRONTEND SETUP (First Time) ─────────────────────────────┐"
echo "│"
echo "│ $ cd frontend"
echo "│ $ npm install"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 5: FRONTEND RUN (Every time)
# ============================================================

echo "┌─ FRONTEND RUN (Every Time) ───────────────────────────────┐"
echo "│"
echo "│ Step 1: Navigate to frontend"
echo "│    $ cd frontend"
echo "│"
echo "│ Step 2: Start development server"
echo "│    $ npm run dev"
echo "│"
echo "│    Expected output:"
echo "│    > ▲ Next.js 14.0.0"
echo "│    > - Local: http://localhost:3000"
echo "│"
echo "│    Open in browser: http://localhost:3000"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 6: VERIFICATION
# ============================================================

echo "┌─ VERIFICATION ─────────────────────────────────────────────┐"
echo "│"
echo "│ Check backend health:"
echo "│    $ curl http://localhost:8000/health"
echo "│"
echo "│ Or run Python verification:"
echo "│    $ python verify_setup.py"
echo "│"
echo "│ Test API generation:"
echo "│    $ curl -X POST http://localhost:8000/generate \\"
echo "│        -H 'Content-Type: application/json' \\"
echo "│        -d '{\"topic\": \"Machine Learning\"}'"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 7: COMPLETE STARTUP SEQUENCE
# ============================================================

echo "┌─ COMPLETE STARTUP (3 Terminal Windows) ──────────────────┐"
echo "│"
echo "│ TERMINAL 1: Start Ollama"
echo "│    $ ollama serve"
echo "│"
echo "│    Wait for: \"Listening on 127.0.0.1:11434\""
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ TERMINAL 2: Start Backend (in new terminal)"
echo "│    $ cd backend"
echo "│    $ source venv/bin/activate"
echo "│    $ python main.py"
echo "│"
echo "│    Wait for: \"Application startup complete\""
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ TERMINAL 3: Start Frontend (in new terminal)"
echo "│    $ cd frontend"
echo "│    $ npm run dev"
echo "│"
echo "│    Wait for: \"▲ Next.js running\""
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ THEN: Open http://localhost:3000 in browser"
echo "│"
echo "│ 🎉 Ready to generate SEO content!"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 8: TROUBLESHOOTING
# ============================================================

echo "┌─ TROUBLESHOOTING ──────────────────────────────────────────┐"
echo "│"
echo "│ Problem: \"Cannot connect to Ollama\""
echo "│   Solution:"
echo "│   1. Ensure Ollama is running: ollama serve"
echo "│   2. Verify: curl http://localhost:11434/api/tags"
echo "│   3. Check Models: ollama list"
echo "│   4. Pull phi if needed: ollama pull phi"
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ Problem: Port already in use"
echo "│   Backend (8000): lsof -i :8000 | kill -9 <PID>"
echo "│   Frontend (3000): lsof -i :3000 | kill -9 <PID>"
echo "│   Ollama (11434): lsof -i :11434 | kill -9 <PID>"
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ Problem: Frontend can't connect to backend"
echo "│   Solution:"
echo "│   1. Check backend is running: http://localhost:8000/health"
echo "│   2. Check CORS is enabled in main.py"
echo "│   3. Verify API_URL in frontend/.env"
echo "│"
echo "├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤"
echo "│"
echo "│ Problem: Slow content generation"
echo "│   Normal: First generation takes 30-60 seconds"
echo "│   Reason: Model loading + inference time"
echo "│   Solution: Subsequent requests are faster (10-30s)"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 9: USEFUL COMMANDS
# ============================================================

echo "┌─ USEFUL COMMANDS ──────────────────────────────────────────┐"
echo "│"
echo "│ Database:"
echo "│   $ sqlite3 backend/kars_seo.db"
echo "│   > .tables"
echo "│   > SELECT * FROM content LIMIT 5;"
echo "│   > .quit"
echo "│"
echo "│ Backend Logs:"
echo "│   $ ps aux | grep python"
echo "│"
echo "│ Clear Database:"
echo "│   $ rm backend/kars_seo.db"
echo "│   (Recreates on backend restart)"
echo "│"
echo "│ Activate Python Environment:"
echo "│   $ cd backend && source venv/bin/activate"
echo "│"
echo "│ Deactivate Python Environment:"
echo "│   $ deactivate"
echo "│"
echo "│ View Running Processes:"
echo "│   $ ps aux | grep ollama"
echo "│   $ ps aux | grep python"
echo "│   $ ps aux | grep node"
echo "│"
echo "│ Kill Processes:"
echo "│   $ pkill -f \"ollama serve\""
echo "│   $ pkill -f \"python main.py\""
echo "│   $ pkill -f \"npm run dev\""
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# ============================================================
# SECTION 10: QUICK REFERENCE
# ============================================================

echo "┌─ QUICK REFERENCE ──────────────────────────────────────────┐"
echo "│"
echo "│ Frontend:        http://localhost:3000"
echo "│ Backend:         http://localhost:8000"
echo "│ Swagger UI:      http://localhost:8000/docs"
echo "│ Ollama:          http://localhost:11434"
echo "│"
echo "│ Database:        backend/kars_seo.db (SQLite)"
echo "│ Python venv:     backend/venv/"
echo "│ Node modules:    frontend/node_modules/"
echo "│"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

echo "✅ For more details, see README.md and API_TESTING.md"
echo ""
