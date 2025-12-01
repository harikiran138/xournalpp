#!/bin/bash

# Kill existing processes on ports
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5002 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "🚀 Starting NovaBoard Demo Environment..."

# 1. Start Main Backend
echo "Starting Backend (Port 5001)..."
cd backend
python3 app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 2. Start Recording Daemon
echo "Starting Recording Daemon (Port 5002)..."
cd backend
python3 daemon.py > ../daemon.log 2>&1 &
DAEMON_PID=$!
cd ..

# 3. Start Frontend
echo "Starting Frontend (Port 3000)..."
yarn start > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "✅ Services Started!"
echo "Backend PID: $BACKEND_PID"
echo "Daemon PID: $DAEMON_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Access the app at http://localhost:3000"
echo "Logs are in backend.log, daemon.log, and frontend.log"
echo ""
echo "Press Ctrl+C to stop all services."

trap "kill $BACKEND_PID $DAEMON_PID $FRONTEND_PID; exit" INT

wait
