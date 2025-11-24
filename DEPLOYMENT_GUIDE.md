# 🚀 Deployment Guide - LipNet Application

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Easiest - Recommended)

**Steps:**
1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy!

**Your app will be live at:** `https://your-app-name.streamlit.app`

---

### Option 2: Render.com (Free Tier Available)

**Steps:**
1. Create account at https://render.com
2. Connect GitHub repository
3. Create two services:
   - **Backend:** Use `render.yaml` configuration
   - **Frontend:** Use `render.yaml` configuration
4. Deploy!

**Your app will be live at:** `https://your-app-name.onrender.com`

---

### Option 3: Railway.app

**Steps:**
1. Create account at https://railway.app
2. Connect GitHub repository
3. Deploy using `Procfile`
4. Your app will be live automatically!

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables configured
- [ ] Model weights uploaded or accessible
- [ ] API URLs updated for production
- [ ] CORS configured correctly

---

## 🔧 Environment Variables

Set these in your deployment platform:

- `API_URL` - Backend API URL (for frontend)
- `PYTHON_VERSION` - Python version (3.11.9)

---

## 📝 Quick Deploy Commands

### For Streamlit Cloud:
Just push to GitHub and connect!

### For Render:
```bash
# Already configured in render.yaml
```

### For Railway:
```bash
railway up
```

---

## ✅ After Deployment

Your application will be accessible via HTTP link like:
- `https://your-app.streamlit.app` (Streamlit Cloud)
- `https://your-app.onrender.com` (Render)
- `https://your-app.railway.app` (Railway)

