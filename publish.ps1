# PowerShell script to publish to GitHub
Write-Host "=== Publishing TalentKonnect/Dompell to GitHub ===" -ForegroundColor Green
Write-Host ""

# Set location
Set-Location "c:\Users\Ella\Desktop\TalentKonnect Project Designs and Code"

# Check if Git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Initialize repository if needed
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init

# Check current status
Write-Host "Current Git status:" -ForegroundColor Yellow
git status

# Remove existing origin if it exists
Write-Host "Setting up remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/lazy-logic/presentation.git

# Verify remote was added
Write-Host "Remote repositories:" -ForegroundColor Yellow
git remote -v

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Check what will be committed
Write-Host "Files to be committed:" -ForegroundColor Yellow
git status --porcelain

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Dompell TalentKonnect application with modern UI and API integration"

# Set main branch
Write-Host "Setting up main branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host "SUCCESS: Code published to https://github.com/lazy-logic/presentation" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to push to GitHub. You may need to authenticate." -ForegroundColor Red
    Write-Host "Try running: git push -u origin main" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Publication Complete ===" -ForegroundColor Green
