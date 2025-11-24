"""Streamlit Frontend for LipNet Application"""
import streamlit as st
import requests
import os
import cv2
import numpy as np
import tempfile
from PIL import Image
import time

# Page configuration with custom icon
st.set_page_config(
    page_title="LipNet - Lip Reading App",
    page_icon="👄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/your-repo/lipnet',
        'Report a bug': 'https://github.com/your-repo/lipnet/issues',
        'About': "LipNet - Advanced Lip Reading Application using Deep Learning"
    }
)

# Backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "session_token" not in st.session_state:
    st.session_state.session_token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

def login(username: str, password: str):
    """Login function"""
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            auth=(username, password),
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.session_token = data.get("session_token")
            st.session_state.username = username
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def logout():
    """Logout function"""
    if st.session_state.session_token:
        try:
            requests.post(
                f"{API_URL}/api/auth/logout",
                params={"session_token": st.session_state.session_token},
                timeout=5
            )
        except:
            pass
    st.session_state.logged_in = False
    st.session_state.session_token = None
    st.session_state.username = None
    st.session_state.camera_active = False

# Sign-in Page
if not st.session_state.logged_in:
    # Header with icon and branding
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.markdown("### 👄")
    with col_title:
        st.title("LipNet - Lip Reading Application")
    
    st.markdown("---")
    st.markdown("### 🧠 Powered by Deep Learning & TensorFlow")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Sign In")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_button:
                if username and password:
                    if login(username, password):
                        st.success("Login successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
        
        st.markdown("---")
        st.info("**Demo Credentials:**\n- Username: `admin` / Password: `admin123`\n- Username: `user` / Password: `user123`")
    
    st.stop()

# Main Application (after login)
st.sidebar.title("👄 LipNet")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 Logged in as:** {st.session_state.username}")
st.sidebar.markdown("---")

# Show deployment link if available
deployment_url = os.getenv("STREAMLIT_URL", "")
if deployment_url:
    st.sidebar.markdown("### 🌐 Live Application")
    st.sidebar.markdown(f"[🔗 Access Web App]({deployment_url})")
    st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Application Info")
st.sidebar.info("""
**LipNet** is an advanced lip reading application that uses deep learning to predict speech from video.

**Features:**
- 📤 Video Upload
- 📹 Realtime Camera
- 🤖 AI Predictions
""")

if st.sidebar.button("Logout", use_container_width=True):
    logout()
    st.rerun()

# Main content with header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>👄 LipNet</h1>
    <p style='color: white; margin: 5px 0;'>Advanced Lip Reading Application</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Tabs for different modes
tab1, tab2 = st.tabs(["📤 Upload Video", "📹 Realtime Camera"])

# Tab 1: Upload Video
with tab1:
    st.header("Upload Video for Prediction")
    st.markdown("Upload a video file (.mpg, .mp4) to get lip reading prediction")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mpg', 'mp4', 'avi', 'mov'],
        help="Upload a video file containing lip movements"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mpg') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Display video
            st.video(uploaded_file)
            
            # Run prediction button
            if st.button("🚀 Run Prediction", use_container_width=True, type="primary"):
                with st.spinner("Processing video and making prediction..."):
                    try:
                        # Upload to backend
                        with open(tmp_path, 'rb') as f:
                            files = {'file': (uploaded_file.name, f, 'video/mpeg')}
                            params = {"session_token": st.session_state.session_token}
                            response = requests.post(
                                f"{API_URL}/api/predict/upload",
                                files=files,
                                params=params,
                                timeout=60
                            )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Prediction Complete!")
                            
                            with col2:
                                st.subheader("📊 Prediction Result")
                                st.markdown("---")
                                st.markdown(f"### **Predicted Text:**")
                                st.info(f'**"{result["prediction"]}"**')
                                
                                st.markdown("---")
                                st.metric("Frames Processed", result.get("frames_processed", 0))
                                st.metric("Video Shape", str(result.get("video_shape", [])))
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend server. Please ensure the backend is running on port 8000.")
                        st.info("To start the backend, run: `python backend/main.py`")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    finally:
                        # Clean up
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
        else:
            st.info("👆 Please upload a video file to get started")

# Tab 2: Realtime Camera
with tab2:
    st.header("Realtime Camera Lip Tracking")
    st.markdown("**Note:** This is a dummy implementation. Real-time camera tracking is in development.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Camera Control")
        
        if st.button("📹 Start Camera", use_container_width=True, type="primary"):
            st.session_state.camera_active = True
            st.info("Camera started (dummy mode)")
        
        if st.button("⏹️ Stop Camera", use_container_width=True):
            st.session_state.camera_active = False
            st.info("Camera stopped")
    
    with col2:
        if st.session_state.camera_active:
            st.subheader("Live Feed")
            # Dummy camera feed
            placeholder = st.empty()
            
            # Simulate camera frames
            for i in range(10):
                # Create dummy frame
                dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                placeholder.image(dummy_frame, caption=f"Frame {i+1} (Dummy)", use_container_width=True)
                time.sleep(0.5)
                
                if not st.session_state.camera_active:
                    break
            
            if st.button("🚀 Run Realtime Prediction", use_container_width=True, type="primary"):
                with st.spinner("Processing realtime frames..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/api/predict/realtime",
                            json={"frame_count": 10},
                            params={"session_token": st.session_state.session_token},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Realtime Prediction Complete!")
                            st.info(f'**Prediction:** "{result["prediction"]}"')
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend server.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info("👆 Click 'Start Camera' to begin realtime tracking")

# Footer with links
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**👄 LipNet Application**")
with col2:
    st.markdown("Built with **Streamlit** & **FastAPI**")
with col3:
    st.markdown("Powered by **TensorFlow** & **Deep Learning**")

# Add social links or website link if deployed
st.markdown("""
<div style='text-align: center; padding: 10px;'>
    <p>🌐 <strong>Live Application</strong> | 
    <a href='https://your-app.streamlit.app' target='_blank'>Access Web App</a></p>
</div>
""", unsafe_allow_html=True)

