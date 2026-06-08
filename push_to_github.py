#!/usr/bin/env python3
"""
Script to push code to GitHub repository.
Run this script after making changes to your code.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None, ignore_error: bool = False) -> None:
    """Run a shell command and print it."""
    cmd_str = " ".join(cmd)
    print(f"🚀 Running: {cmd_str}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr and not ignore_error:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0 and not ignore_error:
        raise RuntimeError(f"Command failed: {cmd_str}\n{result.stderr}")


def main():
    """Main function to push to GitHub."""
    project_root = Path(__file__).parent.resolve()

    print("=" * 60)
    print("🚀 PUSH TO GITHUB")
    print("=" * 60)
    print(f"📁 Project root: {project_root}")
    print()

    # Initialize Git repo
    git_dir = project_root / ".git"
    if not git_dir.exists():
        print("📦 Initializing Git repository...")
        run_command(["git", "init"], cwd=project_root)
        print("✅ Git repository initialized")
        print()

    # Configure Git user
    print("🔧 Configuring Git user...")
    run_command(["git", "config", "user.name", "huydigiwork-source"], cwd=project_root)
    run_command(["git", "config", "user.email", "your_email@example.com"], cwd=project_root)
    print("✅ Git user configured")
    print()

    # Add remote
    print("🔗 Adding GitHub remote...")
    run_command(["git", "remote", "remove", "origin"], cwd=project_root, ignore_error=True)
    run_command([
        "git", "remote", "add", "origin",
        "https://github.com/huydigiwork-source/ecommerce-intelligent.git"
    ], cwd=project_root)
    print("✅ Remote added")
    print()

    # Add all files
    print("📝 Staging all files...")
    run_command(["git", "add", "."], cwd=project_root)
    print("✅ Files staged")
    print()

    # Check for changes
    print("🔍 Checking for changes...")
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=project_root,
        capture_output=True
    )

    if result.returncode == 0:
        print("⚠️  No changes to commit")
        return

    print("✅ Changes detected")
    print()

    # Commit
    print("💾 Committing changes...")
    run_command(["git", "commit", "-m", "Update code via CI/CD script"], cwd=project_root)
    print("✅ Changes committed")
    print()

    # Set main branch
    print("🌿 Setting main branch...")
    run_command(["git", "branch", "-M", "main"], cwd=project_root)
    print("✅ Main branch set")
    print()

    # Pull from GitHub (to merge remote changes)
    print("📥 Pulling from GitHub...")
    run_command(["git", "pull", "origin", "main", "--allow-unrelated-histories"], cwd=project_root, ignore_error=True)
    print("✅ Pulled from GitHub")
    print()

    # Push to GitHub
    print("🚀 Pushing to GitHub...")
    run_command(["git", "push", "-u", "origin", "main"], cwd=project_root)
    print("✅ Pushed to GitHub successfully!")
    print()

    print("=" * 60)
    print("🎉 DONE! Your code is now on GitHub:")
    print("🔗 https://github.com/huydigiwork-source/ecommerce-intelligent")
    print("=" * 60)


if __name__ == "__main__":
    main()