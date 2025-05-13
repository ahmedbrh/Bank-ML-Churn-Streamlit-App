import os
import subprocess
import sys
from threading import Thread
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from api.main import app as api_app

# Configuration variables with environment variable fallbacks
PORT = int(os.environ.get("PORT", 8000))
IS_DEVELOPMENT = os.environ.get("ENVIRONMENT", "development") == "development"

# Configure FastAPI main app that includes the API
app = FastAPI()

# Include the API routes
app.mount("/api", api_app)

# Add root route to redirect to Streamlit
@app.get("/")
async def root():
    if IS_DEVELOPMENT:
        # In development, redirect to the Streamlit port
        return RedirectResponse(url="http://localhost:8501")
    else:
        # In production on Render, redirect to the same host but /streamlit path
        return RedirectResponse(url="/streamlit")

# Function to start the FastAPI server
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=PORT)

# Function to start the Streamlit server
def start_streamlit():
    sys.path.insert(0, os.path.abspath("frontend"))
    
    # In production mode on Render, we need Streamlit to use the same port
    # but a different path
    if not IS_DEVELOPMENT:
        os.environ["STREAMLIT_SERVER_BASE_URL_PATH"] = "streamlit"
        os.environ["STREAMLIT_SERVER_PORT"] = str(PORT)
        # Start Streamlit on the same port but a different base URL path
        subprocess.run([
            "streamlit", "run", "frontend/app.py",
            "--server.port", str(PORT),
            "--server.baseUrlPath", "streamlit",
            "--browser.serverAddress", "0.0.0.0",
            "--server.enableCORS", "true",
            "--server.enableXsrfProtection", "false"
        ])
    else:
        # For development, use separate ports
        subprocess.run([
            "streamlit", "run", "frontend/app.py",
            "--browser.serverAddress", "0.0.0.0"
        ])

# Update the Streamlit API URL based on environment
def update_streamlit_api_url():
    app_path = "frontend/app.py"
    if os.path.exists(app_path):
        with open(app_path, "r") as f:
            content = f.read()
        
        # For production, use relative URL to the API
        if "API_URL =" in content and not IS_DEVELOPMENT:
            updated_content = content.replace(
                'API_URL = "http://localhost:8000/predict"',
                'API_URL = "/api/predict"'
            )
            with open(app_path, "w") as f:
                f.write(updated_content)

if __name__ == "__main__":
    # Update Streamlit config for deployment
    update_streamlit_api_url()
    
    if IS_DEVELOPMENT:
        # In development, run both servers in separate processes
        api_thread = Thread(target=start_api)
        api_thread.daemon = True
        api_thread.start()
        start_streamlit()
    else:
        # In production on Render, we can only bind to a single port
        # Start the FastAPI server
        start_api() 