#!/bin/bash
# UI-REFACTOR-GOLD-2025: Elite dashboard smoke test

set -e

echo "🧪 Starting LexCura Elite Dashboard Smoke Test..."

# Install dependencies
echo "📦 Installing dependencies..."
python -m pip install -r requirements.txt

# Start server in background
echo "🚀 Starting server..."
gunicorn app:server --bind 0.0.0.0:8050 --daemon --pid smoke_test.pid

# Wait for server to start
echo "⏳ Waiting for server startup..."
sleep 5

# Test health endpoint
echo "🩺 Testing health endpoint..."
if curl -f http://localhost:8050/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $(cat smoke_test.pid) 2>/dev/null || true
    rm -f smoke_test.pid
    exit 1
fi

# Test main page
echo "🏠 Testing main dashboard..."
if curl -f http://localhost:8050/ > /dev/null 2>&1; then
    echo "✅ Dashboard loads successfully"
else
    echo "❌ Dashboard failed to load"
    kill $(cat smoke_test.pid) 2>/dev/null || true
    rm -f smoke_test.pid
    exit 1
fi

# Cleanup
echo "🧹 Cleaning up..."
kill $(cat smoke_test.pid) 2>/dev/null || true
rm -f smoke_test.pid

echo "🎉 All smoke tests passed! Elite dashboard is ready for deployment."
exit 0
