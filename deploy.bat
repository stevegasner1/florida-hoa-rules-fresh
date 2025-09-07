@echo off
echo ================================================================
echo          Dynamic HOA Rules Lookup - Quick Deploy Script
echo ================================================================
echo.
echo This script will help you deploy your HOA Rules Lookup system
echo to various cloud platforms.
echo.

:MENU
echo Choose your deployment platform:
echo.
echo 1. Test locally (recommended first)
echo 2. Deploy to Streamlit Cloud (free, recommended)
echo 3. Deploy to Heroku
echo 4. Build Docker image
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto LOCAL
if "%choice%"=="2" goto STREAMLIT
if "%choice%"=="3" goto HEROKU
if "%choice%"=="4" goto DOCKER
if "%choice%"=="5" goto EXIT

echo Invalid choice. Please try again.
goto MENU

:LOCAL
echo.
echo ================================================================
echo                        Testing Locally
echo ================================================================
echo.
echo Starting local Streamlit server...
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run dynamic_hoa_app.py
goto MENU

:STREAMLIT
echo.
echo ================================================================
echo                  Deploying to Streamlit Cloud
echo ================================================================
echo.
echo Steps to deploy to Streamlit Cloud (FREE):
echo.
echo 1. Push your code to GitHub
echo 2. Go to: https://share.streamlit.io
echo 3. Sign in with GitHub
echo 4. Click "New app"
echo 5. Select this repository
echo 6. Set main file: dynamic_hoa_app.py
echo 7. Click "Deploy"
echo.
echo Your app will be available at: https://yourapp.streamlit.app
echo.
pause
goto MENU

:HEROKU
echo.
echo ================================================================
echo                    Deploying to Heroku
echo ================================================================
echo.
echo Make sure you have Heroku CLI installed, then run:
echo.
echo   heroku login
echo   heroku create your-hoa-lookup-app
echo   git push heroku main
echo.
echo Your app will be available at: https://your-hoa-lookup-app.herokuapp.com
echo.
pause
goto MENU

:DOCKER
echo.
echo ================================================================
echo                    Building Docker Image
echo ================================================================
echo.
echo Building Docker image...
docker build -t hoa-lookup .
echo.
echo To run the container locally:
echo   docker run -p 8501:8501 hoa-lookup
echo.
echo To push to a registry:
echo   docker tag hoa-lookup your-registry/hoa-lookup
echo   docker push your-registry/hoa-lookup
echo.
pause
goto MENU

:EXIT
echo.
echo Thank you for using Dynamic HOA Rules Lookup!
echo For detailed deployment instructions, see DEPLOYMENT.md
echo.
exit /b 0