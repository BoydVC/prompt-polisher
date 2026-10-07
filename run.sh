#!/usr/bin/env bash
# Rebuild from the bots' current prompts, then (re)start the viewer on :4270 under nohup.
cd "$(dirname "$0")"
python3 build.py
if [ -f data/server.pid ]; then kill "$(cat data/server.pid)" 2>/dev/null; sleep 0.5; fi
nohup python3 server.py > data/server.log 2>&1 &
echo $! > data/server.pid
sleep 1.2; curl -s http://127.0.0.1:4270/health && echo " → http://127.0.0.1:4270/"
