#!/usr/bin/env bash
# PDF + screenshots with headless Chrome. Needs the server running (./run.sh).
cd "$(dirname "$0")"
C="google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --user-data-dir=/tmp/prompt-polisher-chrome --virtual-time-budget=3000"
$C --no-pdf-header-footer --print-to-pdf=dist/prompt-polisher-summary.pdf "file://$PWD/dist/summary.html" 2>/dev/null
U=http://127.0.0.1:4270/
$C --window-size=1500,1900 --screenshot=screenshots/00-best-jim-podcast-duplicate-diff.png "${U}#bot=Jim&focus=routine-1" 2>/dev/null
$C --window-size=1500,1900 --screenshot=screenshots/01-fleet-top10.png "${U}#fleet" 2>/dev/null
$C --window-size=1500,1900 --screenshot=screenshots/02-pam-stale-items-diff.png "${U}#bot=Pam&focus=routine-0" 2>/dev/null
$C --window-size=1500,1900 --screenshot=screenshots/03-vic-tutor-conflict.png "${U}#bot=Vic%20Tutor" 2>/dev/null
$C --window-size=1500,1900 --screenshot=screenshots/04-oscar-inline-diff.png "${U}#bot=Oscar&focus=routine-0&mode=inline" 2>/dev/null
$C --window-size=390,1800 --force-device-scale-factor=2 --screenshot=screenshots/05-phone-fleet.png "${U}#fleet" 2>/dev/null
ls -la dist screenshots
