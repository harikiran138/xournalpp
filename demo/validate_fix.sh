#!/bin/bash

echo "🧪 Running Post-Fix Validation..."

# 1. Test API Health
echo "Checking API Endpoints..."
curl -f -s http://localhost:5001/api/models/ > /dev/null && echo "✅ /api/models OK" || echo "❌ /api/models FAILED"
curl -f -s http://localhost:5002/api/recording/state > /dev/null && echo "✅ /api/recordings OK" || echo "❌ /api/recordings FAILED"

# 2. Test DB Write Path (Simulate Recording & Section)
echo "Testing DB Write..."
# Create a dummy recording and capture ID
REC_RESPONSE=$(curl -s -X POST http://localhost:5001/api/recordings/ \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Test Recording\", \"filepath\": \"/tmp/test.mp4\"}")
REC_ID=$(echo $REC_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Created Recording ID: $REC_ID"

# Create a dummy section
curl -s -X POST http://localhost:5001/api/recordings/$REC_ID/sections \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Test Section\", \"start_ms\": 0, \"end_ms\": 1000}" > /dev/null

# Verify in DB
COUNT=$(sqlite3 backend/instance/novaboard.db "SELECT count(*) FROM section WHERE recording_id='$REC_ID';")
if [ "$COUNT" -eq 1 ]; then
    echo "✅ DB Write (Section) OK"
else
    echo "❌ DB Write (Section) FAILED"
fi

# 3. Test Model Annotation Endpoint
echo "Testing Annotation Endpoint..."
# Get first model ID
MODEL_ID=$(curl -s http://localhost:5001/api/models/ | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
echo "Testing Model ID: $MODEL_ID"

if [ -z "$MODEL_ID" ]; then
    echo "❌ No models found to test annotations."
else
    # Add annotation
    curl -s -X POST http://localhost:5001/api/models/$MODEL_ID/annotations \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"Test Note\", \"position\": {\"x\":0, \"y\":0, \"z\":0}}" > /dev/null
    
    # Verify annotation exists (by checking metadata)
    # We need to fetch the specific model or list again
    HAS_NOTE=$(curl -s http://localhost:5001/api/models/ | grep "Test Note")
    if [ -n "$HAS_NOTE" ]; then
        echo "✅ Annotation Persistence OK"
    else
        echo "❌ Annotation Persistence FAILED"
    fi
fi

echo "✨ Validation Complete!"
