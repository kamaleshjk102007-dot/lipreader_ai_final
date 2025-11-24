@echo off
echo ========================================
echo   LipNet Deployment Setup
echo ========================================
echo.
echo This will help you deploy your app to get an HTTP link!
echo.
pause

echo.
echo Step 1: Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo Git already initialized or not installed
)

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit - LipNet application ready for deployment"

echo.
echo ========================================
echo   Next Steps to Deploy:
echo ========================================
echo.
echo 1. Create a GitHub repository:
echo    - Go to: https://github.com/new
echo    - Create a new repository (name it: lipnet-app)
echo    - Don't initialize with README
echo.
echo 2. Push your code:
echo    git remote add origin https://github.com/YOUR-USERNAME/lipnet-app.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy to Streamlit Cloud:
echo    - Go to: https://share.streamlit.io
echo    - Sign in with GitHub
echo    - Click "New app"
echo    - Select your repository
echo    - Main file: frontend/app.py
echo    - Click "Deploy"
echo.
echo 4. Get your HTTP link:
echo    https://your-app-name.streamlit.app
echo.
echo ========================================
pause

