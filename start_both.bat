@echo off
echo Starting Library Management System...
echo.
echo Main System: http://localhost:5000
echo File Viewer: http://localhost:5001
echo.
echo Press Ctrl+C to stop both applications
echo.

start "Library System" cmd /k "cd /d %~dp0 && python run.py"
start "File Viewer" cmd /k "cd /d %~dp0file_viewer && python app_simple.py"

echo Both applications started!
echo Close this window or press any key to exit...
pause