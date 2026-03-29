#!/usr/bin/env python3
"""
Circuit Forge Play - Deployment Script
Automates the process of committing and pushing changes to trigger Streamlit Cloud deployment.

Usage:
    python deploy.py "commit message"

This script will:
1. Add all changes to git
2. Commit with the provided message
3. Push to the current branch
4. Display deployment information

The push will automatically trigger:
- GitHub Actions workflow (.github/workflows/deploy-streamlit.yml)
- Validation of code and dependencies
- Automatic Streamlit Cloud deployment
- Live app update at: https://circuit-forge-play-app31.streamlit.app/
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description):
    """Run a shell command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False, e.stderr

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Please provide a commit message")
        print("Usage: python deploy.py \"Your commit message\"")
        sys.exit(1)

    commit_message = sys.argv[1]

    print("🚀 Circuit Forge Play - Deployment Script")
    print("=" * 50)
    print(f"Commit message: {commit_message}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check git status
    success, output = run_command("git status --porcelain", "Checking git status")
    if not success:
        sys.exit(1)

    if not output.strip():
        print("⚠️  No changes to commit. Exiting.")
        sys.exit(0)

    print(f"📝 Changes to commit:\n{output}")

    # Add all changes
    success, _ = run_command("git add -A", "Adding all changes")
    if not success:
        sys.exit(1)

    # Commit
    success, _ = run_command(f'git commit -m "{commit_message}"', "Committing changes")
    if not success:
        sys.exit(1)

    # Push
    success, _ = run_command("git push origin HEAD", "Pushing to remote repository")
    if not success:
        sys.exit(1)

    print()
    print("🎉 Deployment process completed successfully!")
    print()
    print("📋 What happens next:")
    print("1. GitHub Actions workflow will validate the code")
    print("2. Streamlit Cloud will auto-detect changes and redeploy")
    print("3. App will be live at: https://circuit-forge-play-app31.streamlit.app/")
    print()
    print("⏱️  Estimated deployment time: 2-5 minutes")
    print("🔍 Check deployment status:")
    print("   - GitHub Actions: https://github.com/rishabh-iitbhu/circuit-forge-play/actions")
    print("   - Streamlit Cloud: https://share.streamlit.io/")
    print()
    print("🔧 If you need to configure secrets:")
    print("   - Go to Streamlit Cloud app settings")
    print("   - Add OPENAI_API_KEY and other required secrets")
    print("   - Reference: .streamlit/secrets.example.toml")

if __name__ == "__main__":
    main()