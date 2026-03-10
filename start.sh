#!/bin/bash
set -e

# Start Rust API in background
cd /app
uet_api &
API_PID=$!

# Start Next.js frontend
cd /app/uet_web
npm start &
WEB_PID=$!

# Wait for either process to exit
wait -n $API_PID $WEB_PID

# Kill remaining process and exit
kill $(jobs -p) 2>/dev/null || true
exit 1
