@echo off
set COMMIT_MSG=%1
nif "%COMMIT_MSG%"=="" set COMMIT_MSG=Auto-deploy: update from local workspace
cd /d %~dp0\..
echo Adding changes...
git add -A
ngit commit -m "%COMMIT_MSG%"
echo Pushing to origin main...
git push origin main
pause