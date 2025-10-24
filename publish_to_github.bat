@echo off
echo Publishing TalentKonnect/Dompell project to GitHub...
echo.

echo Step 1: Initializing Git repository...
git init

echo Step 2: Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/lazy-logic/presentation.git

echo Step 3: Adding all files...
git add .

echo Step 4: Committing changes...
git commit -m "Initial commit: Dompell TalentKonnect application with modern UI and API integration"

echo Step 5: Setting up main branch...
git branch -M main

echo Step 6: Pushing to GitHub...
git push -u origin main

echo.
echo Publishing complete! Your code should now be available at:
echo https://github.com/lazy-logic/presentation
echo.
pause
