#!/bin/bash

# Setup script for arXiv Paper Summarizer

echo "========================================="
echo "arXiv Paper Summarizer - Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env and add your API keys and configuration"
else
    echo ""
    echo ".env file already exists"
fi

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your credentials:"
echo "   - ANTHROPIC_API_KEY"
echo "   - NOTION_TOKEN"
echo "   - NOTION_DATABASE_ID"
echo ""
echo "2. Run the application:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Or run with scheduler:"
echo "   python scheduler.py"
echo ""
