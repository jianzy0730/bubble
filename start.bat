@echo off
setlocal
set PORT=3000

echo Starting bubble backend on port %PORT%...
echo (first run will install dependencies)

if not exist node_modules (
  npm install
  if errorlevel 1 (
    echo npm install failed. Press any key to exit.
    pause >nul
    exit /b 1
  )
)

start http://localhost:%PORT%/
npm start
