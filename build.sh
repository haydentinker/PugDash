#!/bin/bash
set -e

echo "Starting pygbag server..."
python3 -m pygbag --build src/main.py &
PYGBAG_PID=$!

echo "Waiting for server to come up..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "Server ready after ${i}s"
        break
    fi
    sleep 2
done

echo "Triggering build via HTTP request..."
curl -s http://localhost:8000/ > /dev/null 2>&1 || true

echo "Polling for build output..."
TIMEOUT=300
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    if [ -f "src/build/web/index.html" ]; then
        echo "index.html found at ${ELAPSED}s — waiting for full package..."
        sleep 30
        break
    fi
    echo "  ${ELAPSED}s — not ready yet..."
    sleep 5
    ELAPSED=$((ELAPSED + 5))
done

kill $PYGBAG_PID 2>/dev/null || true
wait $PYGBAG_PID 2>/dev/null || true

echo "Build directory contents:"
ls -la src/build/web/ 2>/dev/null || echo "Directory missing"

if [ -f "src/build/web/index.html" ]; then
    echo "Build successful!"
    exit 0
else
    echo "Build failed — index.html not found after ${TIMEOUT}s"
    exit 1
fi
