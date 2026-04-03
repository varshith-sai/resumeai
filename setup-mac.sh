#!/bin/bash

echo "=========================================="
echo "   ResumeAI — Mac Setup Script"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
  echo "❌ Python 3 not found. Install from https://www.python.org/downloads/"
  exit 1
fi

# Check Node.js
echo ""
echo "Checking Node.js version..."
node --version
if [ $? -ne 0 ]; then
  echo "❌ Node.js not found. Install from https://nodejs.org/"
  exit 1
fi

# Check LibreOffice
echo ""
echo "Checking LibreOffice..."
if command -v libreoffice &> /dev/null; then
  echo "✅ LibreOffice found"
elif [ -f "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
  echo "✅ LibreOffice found at /Applications/LibreOffice.app"
  # Add to PATH for this session
  export PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH"
  echo 'export PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH"' >> ~/.zshrc
  echo "✅ LibreOffice added to PATH"
else
  echo "⚠️  LibreOffice not found."
  echo "    Download from: https://www.libreoffice.org/download/download-libreoffice/"
  echo "    Install it, then run this script again."
  exit 1
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-mac.txt

if [ $? -eq 0 ]; then
  echo "✅ Python dependencies installed"
else
  echo "❌ Failed to install Python dependencies"
  exit 1
fi

# Install frontend dependencies
echo ""
echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -eq 0 ]; then
  echo "✅ Frontend dependencies installed"
else
  echo "❌ Failed to install frontend dependencies"
  exit 1
fi
cd ..

# Create config from example
echo ""
if [ ! -f "config.yaml" ]; then
  cp config.example.yaml config.yaml
  echo "✅ config.yaml created from template — edit it with your details"
else
  echo "✅ config.yaml already exists"
fi

# Create .env from example
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "✅ .env created from template — add your API tokens"
else
  echo "✅ .env already exists"
fi

# Create data folder
mkdir -p data output

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your HF_API_TOKEN and GITHUB_TOKEN"
echo "2. Edit config.yaml with your personal details"
echo "3. Add your resume text to data/master_resume.txt"
echo ""
echo "To run the app:"
echo "  Terminal 1: source venv/bin/activate && uvicorn backend.main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo "  Open:       http://localhost:5173"
echo "=========================================="