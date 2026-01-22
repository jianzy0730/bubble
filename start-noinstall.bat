@echo off
setlocal
set PORT=3000

echo Starting standalone server (no npm install needed) on port %PORT%...
start http://localhost:%PORT%/
node server-standalone.js
