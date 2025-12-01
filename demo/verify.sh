#!/bin/bash

echo "🔍 Verifying NovaBoard Model Library..."

# 1. Check DB
echo "Checking Database..."
DB_COUNT=$(sqlite3 backend/instance/novaboard.db "SELECT count(*) FROM model3_d;")
echo "Models in DB: $DB_COUNT"

if [ "$DB_COUNT" -lt 5 ]; then
    echo "❌ Error: Too few models in DB. Ingestion might have failed."
    exit 1
fi

# 2. Check Files
echo "Checking File Storage..."
FILE_COUNT=$(find backend/data/media/models -name "*.glb" | wc -l)
echo "GLB Files found: $FILE_COUNT"

if [ "$FILE_COUNT" -lt 5 ]; then
    echo "❌ Error: Too few GLB files found."
    exit 1
fi

# 3. Check Endpoint
echo "Checking Backend API..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/models/)
echo "API Response Code: $HTTP_CODE"

if [ "$HTTP_CODE" -ne 200 ]; then
    echo "❌ Error: Backend API not reachable or returning error."
    exit 1
fi

echo "✅ Verification Passed!"
exit 0
