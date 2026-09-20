#!/usr/bin/env python3
"""Commit & push the ./docs directory to the current git repo (GitHub Pages source).

Usage:
  python deploy_pages.py "commit message"

Assumptions:
  - The current working directory is a git repo already connected to a GitHub remote.
  - GitHub Pages is configured to serve from branch `master`, folder `/docs`
    (Settings -> Pages -> Branch: master, Folder: /docs).
Prints the resulting public URL after push, and the command to regenerate the public QR.
"""
import os
import subprocess
import sys


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    if len(sys.argv) < 2:
        msg = input("Commit message: ").strip()
    else:
        msg = sys.argv[1]
    repo = os.path.basename(os.getcwd())
    login = ""
    try:
        login = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        login = "<user>"
    try:
        run(["git", "add", "docs"])
        run(["git", "commit", "-m", msg])
        run(["git", "push"])
    except subprocess.CalledProcessError as e:
        sys.exit(f"Git step failed: {e}")
    url = f"https://{login}.github.io/{repo}/"
    print("\nDeployed. Public AR URL:")
    print(" ", url)
    print("Regenerate the public QR with:")
    print(f'  python scripts/qr_generate.py "{url}"')


if __name__ == "__main__":
    main()
