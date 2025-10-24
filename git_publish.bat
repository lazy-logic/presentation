@echo off
echo === Publishing to GitHub ===
cd /d "c:\Users\Ella\Desktop\TalentKonnect Project Designs and Code"

echo Checking Git version...
git --version
if errorlevel 1 (
    echo ERROR: Git not found!
    pause
    exit /b 1
)

echo.
echo Initializing repository...
git init

echo.
echo Current status:
git status

echo.
echo Adding remote...
git remote remove origin 2>nul
git remote add origin https://github.com/lazy-logic/presentation.git

echo.
echo Verifying remote:
git remote -v

echo.
echo Adding files...
git add .

echo.
echo Committing...
git commit -m "Initial commit: Dompell TalentKonnect application"

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. You may need to authenticate with GitHub.
    echo Please run the following command manually:
    echo git push -u origin main
) else (
    echo.
    echo SUCCESS: Published to https://github.com/lazy-logic/presentation
)

echo.
pause
