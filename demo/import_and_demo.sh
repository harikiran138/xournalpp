#!/bin/bash

# Kill existing processes
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5002 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "🚀 Starting NovaBoard Model Ingestion & Demo..."

# 1. Start Backend for Ingestion
echo "Starting Backend..."
cd backend
python3 app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
sleep 5

# 2. Run Ingestion Script
echo "Running Model Ingestion..."
python3 scripts/ingest_models.py

# 3. Start Recording Daemon
echo "Starting Recording Daemon..."
cd backend
python3 daemon.py > ../daemon.log 2>&1 &
DAEMON_PID=$!
cd ..

# 4. Start Frontend
echo "Starting Frontend..."
yarn start > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "✅ Demo Environment Ready!"
echo "Backend PID: $BACKEND_PID"
echo "Daemon PID: $DAEMON_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Access the app at http://localhost:3000"
echo "Open '3D Models' -> 'My Library' to see ingested models."
echo ""
echo "Press Ctrl+C to stop all services."

trap "kill $BACKEND_PID $DAEMON_PID $FRONTEND_PID; exit" INT

wait
