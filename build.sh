#!/bin/bash
set -e

python3 -m pygbag --build src/main.py &
PYGBAG_PID=$!

echo "Waiting for pygbag to build..."
TIMEOUT=300
ELAPSED=0
while [ ! -f "src/build/web/index.html" ] && [ $ELAPSED -lt $TIMEOUT ]; do
    sleep 3
    ELAPSED=$((ELAPSED + 3))
done

# Give it extra time to finish packaging the .apk
sleep 15

kill $PYGBAG_PID 2>/dev/null || true
wait $PYGBAG_PID 2>/dev/null || true

if [ -f "src/build/web/index.html" ]; then
    echo "Build complete:"
    ls src/build/web/
    exit 0
else
    echo "Build failed - index.html not found after ${TIMEOUT}s"
    exit 1
fi
