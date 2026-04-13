#!/bin/bash

# KARS SEO Engine - Quick Start Script
# This script sets up both backend and frontend automatically

echo "🚀 KARS SEO Engine - Quick Start"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo "${YELLOW}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "${RED}Python 3 is not installed${NC}"
    exit 1
fi
echo "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Node
echo ""
echo "${YELLOW}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "${RED}Node.js is not installed${NC}"
    exit 1
fi
echo "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check Ollama
echo ""
echo "${YELLOW}Checking Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "${YELLOW}⚠ Ollama is not installed, but can be set up separately${NC}"
else
    echo "${GREEN}✓ Ollama found: $(ollama --version)${NC}"
fi

# Setup Backend
echo ""
echo "${YELLOW}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing Python dependencies..."
pip install -q -r ../requirements.txt

echo "${GREEN}✓ Backend setup complete${NC}"
cd ..

# Setup Frontend
echo ""
echo "${YELLOW}Setting up Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install -q
fi

echo "${GREEN}✓ Frontend setup complete${NC}"
cd ..

echo ""
echo "${GREEN}================================${NC}"
echo "${GREEN}✅ Setup Complete!${NC}"
echo "${GREEN}================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Ollama (in new terminal):"
echo "   ${YELLOW}ollama serve${NC}"
echo ""
echo "2. Start Backend (in new terminal):"
echo "   ${YELLOW}cd backend && source venv/bin/activate && python main.py${NC}"
echo ""
echo "3. Start Frontend (in new terminal):"
echo "   ${YELLOW}cd frontend && npm run dev${NC}"
echo ""
echo "4. Open in browser: ${YELLOW}http://localhost:3000${NC}"
echo ""
