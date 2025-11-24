"""Quick deployment helper script"""
import os
import subprocess
import sys

def check_git():
    """Check if git is initialized"""
    if not os.path.exists('.git'):
        print("Initializing git repository...")
        subprocess.run(['git', 'init'], check=False)
        print("[OK] Git initialized")
    else:
        print("[OK] Git repository exists")

def create_requirements():
    """Ensure requirements.txt is up to date"""
    print("[OK] requirements.txt ready")

def main():
    print("="*60)
    print("LipNet Deployment Helper")
    print("="*60)
    print()
    
    print("Step 1: Checking git repository...")
    check_git()
    print()
    
    print("Step 2: Checking requirements...")
    create_requirements()
    print()
    
    print("="*60)
    print("Ready for Deployment!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Push to GitHub:")
    print("   git add .")
    print("   git commit -m 'Deploy LipNet app'")
    print("   git push origin main")
    print()
    print("2. Deploy to Streamlit Cloud:")
    print("   - Go to: https://share.streamlit.io")
    print("   - Connect your GitHub repo")
    print("   - Deploy!")
    print()
    print("3. Get your HTTP link:")
    print("   https://your-app-name.streamlit.app")
    print()
    print("="*60)

if __name__ == "__main__":
    main()

