# 🚀 Deploy to Streamlit Cloud (Easiest Method)

## Step-by-Step Guide

### 1. Prepare Your Repository

1. **Create a GitHub repository** (if you don't have one)
   - Go to https://github.com/new
   - Create a new repository named `lipnet-app`

2. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - LipNet app"
   git branch -M main
   git remote add origin https://github.com/your-username/lipnet-app.git
   git push -u origin main
   ```

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Deploy your app:**
   - Click "New app"
   - Select your repository: `your-username/lipnet-app`
   - Main file path: `frontend/app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   ```
   https://your-app-name.streamlit.app
   ```

### 3. Configure Backend (If using separate backend)

If your backend is on a different service:

1. Update `frontend/app.py` line 20:
   ```python
   API_URL = os.getenv("API_URL", "https://your-backend-url.com")
   ```

2. Set environment variable in Streamlit Cloud:
   - Go to app settings
   - Add environment variable: `API_URL = https://your-backend-url.com`

### 4. Access Your Deployed App

Once deployed, you'll get a link like:
```
https://lipnet-app.streamlit.app
```

**Share this link with anyone!** 🌐

---

## 🎨 Custom Domain (Optional)

You can also use a custom domain:
- Go to app settings
- Add custom domain
- Update DNS records

---

## ✅ That's It!

Your app is now live on the internet with an HTTP link!

