import os
import subprocess
import sys
from threading import Thread
import uvicorn
from api.main import app

# Configuration variables with environment variable fallbacks
API_PORT = int(os.environ.get("PORT", 8000))
STREAMLIT_PORT = 8501  # Streamlit's default port
IS_DEVELOPMENT = os.environ.get("ENVIRONMENT", "development") == "development"

# Function to start the FastAPI server
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)

# Function to start the Streamlit server
def start_streamlit():
    sys.path.insert(0, os.path.abspath("frontend"))
    subprocess.run([
        "streamlit", "run", "frontend/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--browser.serverAddress", "0.0.0.0",
        "--server.enableCORS", "false"
    ])

# Update the Streamlit API URL based on environment
def update_streamlit_api_url():
    app_path = "frontend/app.py"
    if os.path.exists(app_path):
        with open(app_path, "r") as f:
            content = f.read()
        
        # For production, use relative URL
        if "API_URL =" in content and not IS_DEVELOPMENT:
            updated_content = content.replace(
                'API_URL = "http://localhost:8000/predict"',
                'API_URL = "/predict"'
            )
            with open(app_path, "w") as f:
                f.write(updated_content)

if __name__ == "__main__":
    # Update Streamlit config for deployment
    update_streamlit_api_url()
    
    # In production, run both servers in the same process
    api_thread = Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Start Streamlit in the main thread
    start_streamlit() 