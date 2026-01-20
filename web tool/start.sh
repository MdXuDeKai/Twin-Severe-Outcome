#!/bin/bash
# Startup Script - Twin Severe Outcome Prediction Web Diagnostic Tool (Linux/Mac)

echo "🚀 Starting Twin Severe Outcome Prediction Web Diagnostic Tool..."
echo ""

# Check Python environment
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Error: Python3 environment not found, please install Python 3.8+"
    exit 1
fi

echo "✅ Python environment check passed"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Dependency installation failed"
    exit 1
fi

echo "✅ Dependencies installation completed"
echo ""

# Start application
echo "🌐 Starting Web application..."
echo "Access URL: http://localhost:5000"
echo "Press Ctrl+C to stop service"
echo ""

python3 app.py


