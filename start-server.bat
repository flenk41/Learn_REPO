@echo off
title Course server - Work with memory
echo.
echo  ============================================
echo    Starting course (C / C++ / Python / Rust / AI)
echo  ============================================
echo.

cd /d "%~dp0"

REM --- Try py launcher first (it avoids the Microsoft Store stub) ---
py --version >nul 2>nul
if %errorlevel%==0 (
    echo  Server running at:  http://localhost:8000
    echo  Opening browser...  close this window to stop the server.
    echo.
    start "" http://localhost:8000
    py -m http.server 8000
    goto :eof
)

REM --- Then python (checked by a real call, not by where) ---
python --version >nul 2>nul
if %errorlevel%==0 (
    echo  Server running at:  http://localhost:8000
    echo  Opening browser...  close this window to stop the server.
    echo.
    start "" http://localhost:8000
    python -m http.server 8000
    goto :eof
)

REM --- Try Node ---
where npx >nul 2>nul
if %errorlevel%==0 (
    echo  Starting via Node (npx serve)...
    npx --yes serve -l 8000
    goto :eof
)

echo  [!] Python and Node.js were not found.
echo.
echo  Install Python from https://python.org  ("Add to PATH" checkbox),
echo  then run this file again.
echo.
pause
