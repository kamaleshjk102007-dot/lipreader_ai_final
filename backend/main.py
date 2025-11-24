"""Backend API for LipNet Application"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import cv2
import tensorflow as tf
import numpy as np
import tempfile
import shutil
from typing import Optional
import secrets
from datetime import datetime, timedelta
import json

# Import model utilities
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

app = FastAPI(title="LipNet API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple authentication (in production, use proper auth)
security = HTTPBasic()

# Dummy user database (in production, use real database)
USERS_DB = {
    "admin": {"password": "admin123", "name": "Admin User"},
    "user": {"password": "user123", "name": "Test User"},
}

# Session management (simple in-memory)
active_sessions = {}

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify user credentials"""
    if credentials.username in USERS_DB:
        if credentials.password == USERS_DB[credentials.username]["password"]:
            # Create session token
            session_token = secrets.token_urlsafe(32)
            active_sessions[session_token] = {
                "username": credentials.username,
                "expires": datetime.now() + timedelta(hours=24)
            }
            return session_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

def get_current_user(session_token: Optional[str] = None):
    """Get current user from session"""
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if session_token not in active_sessions:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    session = active_sessions[session_token]
    if datetime.now() > session["expires"]:
        del active_sessions[session_token]
        raise HTTPException(status_code=401, detail="Session expired")
    
    return session["username"]

# Import LipNet utilities from notebook and scripts
try:
    from lipnet_utils import (
        load_video,
        build_model,
        decode_prediction,
        process_video_for_prediction,
        char_to_num,
        num_to_char,
        vocab
    )
except ImportError:
    # Fallback: import from same directory
    import sys
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, backend_dir)
    from lipnet_utils import (
        load_video,
        build_model,
        decode_prediction,
        process_video_for_prediction,
        char_to_num,
        num_to_char,
        vocab
    )

# Global model variable
model = None

def load_model_weights():
    """Load model weights"""
    global model
    if model is None:
        model = build_model()
        
        # Try to load weights
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        checkpoint_paths = [
            os.path.join(base_dir, 'models', 'models', 'checkpoint'),
            os.path.join(base_dir, 'models', 'checkpoint'),
            'models/models/checkpoint',
            'models/checkpoint'
        ]
        
        weights_loaded = False
        for checkpoint_path in checkpoint_paths:
            if os.path.exists(checkpoint_path + '.index'):
                try:
                    checkpoint = tf.train.Checkpoint(model=model)
                    checkpoint.restore(checkpoint_path).expect_partial()
                    weights_loaded = True
                    break
                except:
                    continue
        
        if not weights_loaded:
            print("Warning: No weights loaded, using untrained model")

# Load model on startup
@app.on_event("startup")
async def startup_event():
    load_model_weights()

@app.get("/")
async def root():
    return {"message": "LipNet API is running", "version": "1.0.0"}

@app.post("/api/auth/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """Login endpoint"""
    session_token = verify_user(credentials)
    return {
        "success": True,
        "session_token": session_token,
        "username": credentials.username,
        "message": "Login successful"
    }

@app.post("/api/auth/logout")
async def logout(session_token: str):
    """Logout endpoint"""
    if session_token in active_sessions:
        del active_sessions[session_token]
    return {"success": True, "message": "Logged out"}

@app.get("/api/auth/verify")
async def verify_session(session_token: str):
    """Verify session token"""
    try:
        username = get_current_user(session_token)
        return {"success": True, "username": username}
    except:
        return {"success": False, "message": "Invalid session"}

@app.post("/api/predict/upload")
async def predict_from_upload(
    file: UploadFile = File(...),
    session_token: Optional[str] = None
):
    """Predict from uploaded video file"""
    try:
        # Verify session (optional for demo)
        # username = get_current_user(session_token)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mpg') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Make prediction using notebook functions
            if model is None:
                load_model_weights()
            
            # Use unified processing function from notebook
            predicted_text, frames = process_video_for_prediction(tmp_path, model)
            
            return {
                "success": True,
                "prediction": predicted_text,
                "frames_processed": int(frames.shape[0]),
                "video_shape": list(frames.shape)
            }
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/predict/realtime")
async def predict_realtime(
    frames_data: dict,
    session_token: Optional[str] = None
):
    """Predict from realtime camera frames (dummy implementation)"""
    try:
        # Verify session (optional for demo)
        # username = get_current_user(session_token)
        
        # Dummy implementation - in real app, process camera frames
        # For now, return a placeholder
        return {
            "success": True,
            "prediction": "realtime prediction (dummy mode)",
            "message": "Realtime camera tracking is in development",
            "frames_received": frames_data.get("frame_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Realtime prediction error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

