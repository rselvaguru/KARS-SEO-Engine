"""
Run this script to test if all components are working correctly
python verify_setup.py
"""

import subprocess
import sys
import json
from urllib.request import urlopen
from urllib.error import URLError

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python: OK (3.10+)")
        return True
    print(f"❌ Python: FAILED (Required 3.10+, got {version.major}.{version.minor})")
    return False

def check_backend():
    """Check if backend is running"""
    try:
        response = urlopen("http://localhost:8000/health", timeout=5)
        data = json.loads(response.read().decode())
        if data.get("status") == "healthy":
            ollama_status = data.get("ollama", "unknown")
            print(f"✅ Backend: OK (Ollama: {ollama_status})")
            return True
    except URLError:
        pass
    except Exception as e:
        print(f"❌ Backend check failed: {e}")
        return False
    
    print("❌ Backend: NOT RUNNING (http://localhost:8000)")
    return False

def check_ollama():
    """Check if Ollama is running and has phi model"""
    try:
        response = urlopen("http://localhost:11434/api/tags", timeout=5)
        data = json.loads(response.read().decode())
        models = [m.get("name", "") for m in data.get("models", [])]
        if any("phi" in m for m in models):
            print(f"✅ Ollama: OK (Available models: {', '.join(models[:3])}...)")
            return True
        print(f"⚠️  Ollama: Running but phi model not found. Run: ollama pull phi")
        return False
    except URLError:
        print("❌ Ollama: NOT RUNNING (http://localhost:11434)")
        return False
    except Exception as e:
        print(f"❌ Ollama check failed: {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = urlopen("http://localhost:3000", timeout=5)
        print("✅ Frontend: OK (http://localhost:3000)")
        return True
    except URLError:
        print("❌ Frontend: NOT RUNNING (http://localhost:3000)")
        return False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return False

def main():
    print("\n🔍 KARS SEO Engine - Verification Check\n")
    print("=" * 50)
    
    results = {
        "Python": check_python(),
        "Ollama": check_ollama(),
        "Backend": check_backend(),
        "Frontend": check_frontend(),
    }
    
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} checks passed\n")
    
    if passed == total:
        print("✅ All systems operational!")
        print("\n🎉 Ready to generate SEO content!")
        return 0
    else:
        print("⚠️  Some components are not running.")
        print("\nTo start all services, run in separate terminals:")
        print("  1. ollama serve")
        print("  2. cd backend && source venv/bin/activate && python main.py")
        print("  3. cd frontend && npm run dev")
        return 1

if __name__ == "__main__":
    sys.exit(main())
