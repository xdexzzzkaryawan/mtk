#!/bin/bash

# Auto Install and Run Bot Script
# This script installs all required packages and runs the bot

set -e  # Exit on any error

echo "================================"
echo "Bot Installation and Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip3 install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip3 install -r requirements.txt
    echo "✅ Dependencies installed successfully"
    echo ""
else
    echo "⚠️  requirements.txt not found. Skipping dependency installation."
    echo ""
fi

# Run the bot
echo "================================"
echo "Starting Bot..."
echo "================================"
echo ""

if [ -f "main.py" ]; then
    echo "🚀 Running bot with main.py..."
    python3 main.py
elif [ -f "bot.py" ]; then
    echo "🚀 Running bot with bot.py..."
    python3 bot.py
elif [ -f "run.py" ]; then
    echo "🚀 Running bot with run.py..."
    python3 run.py
else
    echo "❌ No main entry point found (main.py, bot.py, or run.py)"
    echo "Please specify your bot's main entry point file."
    exit 1
fi
