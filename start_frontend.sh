#!/bin/bash

cd /home/jibin_joby/news-analyzer/frontend

echo "========================================="
echo "Starting Frontend Development Server"
echo "========================================="
echo ""

# Set environment to prevent browser auto-open from WSL
export BROWSER=none

# Start the development server
npm start

echo ""
echo "Frontend is running at http://localhost:3000"
echo "Open this URL in your Windows browser"
echo ""
