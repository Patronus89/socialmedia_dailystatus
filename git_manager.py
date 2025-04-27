# git_manager.py
# Git add, commit, push automation logic here
# git_manager.py
import subprocess
import os

def git_commit_and_push(repo_path, commit_message="Daily Report Update"):
    try:
        current_dir = os.getcwd()
        os.chdir(repo_path)

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)

        print("✅ Git push successful.")
        os.chdir(current_dir)
    except Exception as e:
        print(f"⚠️ Git push failed: {e}")
        os.chdir(current_dir)

print("Pushing report to GitHub...")