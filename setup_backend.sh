#!/bin/bash

echo "========================================"
echo "Setting up Backend Virtual Environment"
echo "========================================"

cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To activate the environment, run:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo ""
echo "Then run the backend:"
echo "  python app.py"
echo ""
