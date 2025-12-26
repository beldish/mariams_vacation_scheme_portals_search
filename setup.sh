#!/bin/bash
# Quick Start Script for Vacation Scheme Search Agent

echo "========================================"
echo "Vacation Scheme Search Agent Setup"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi
echo "✓ pip3 found"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if config.ini exists
if [ ! -f "config.ini" ]; then
    echo ""
    echo "⚠️  Configuration file not found."
    echo "Creating config.ini from template..."
    cp config.ini.example config.ini
    echo ""
    echo "📝 Please edit config.ini and add your credentials:"
    echo "   - SerpAPI key"
    echo "   - Gmail app password"
    echo ""
    echo "Then run this script again or start the agent with:"
    echo "   python3 search_agent.py    # Run once"
    echo "   python3 scheduler.py       # Run scheduler"
    exit 0
fi

# Run tests
echo ""
echo "Running tests..."
python3 test_agent.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Setup complete!"
    echo ""
    echo "You can now:"
    echo "  1. Run a single search:    python3 search_agent.py"
    echo "  2. Start the scheduler:    python3 scheduler.py"
    echo "  3. Install as service:     See README.md for instructions"
else
    echo ""
    echo "❌ Tests failed. Please check your configuration."
    exit 1
fi
