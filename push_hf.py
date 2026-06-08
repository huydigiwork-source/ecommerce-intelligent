#!/usr/bin/env python3
"""
Script để push tất cả file lên Hugging Face Space
Space URL: https://huggingface.co/spaces/Vincentran/ecommerce-intelligence

Sử dụng:
    python push_hf.py
"""

import os
import subprocess
import sys
from pathlib import Path

# Space configuration
USERNAME = "Vincentran"
SPACE_NAME = "ecommerce-intelligence"
SPACE_REPO = f"https://huggingface.co/spaces/{USERNAME}/{SPACE_NAME}"
SPACE_DIR = SPACE_NAME

# Files cần upload
FILES_TO_UPLOAD = [
    "app.py",
    "requirements.txt",
    "Dockerfile"
]

BACKEND_DIR = "backend"


def run_command(cmd, cwd=None):
    """Chạy command và print output."""
    print(f"🚀 Running: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=False,
        text=True
    )
    return result.returncode == 0


def check_hf_cli():
    """Kiểm tra hf đã cài chưa."""
    print("🔍 Checking hf CLI...")
    result = subprocess.run(
        ["hf", "--version"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ hf not found. Installing huggingface_hub...")
        run_command("pip install -U huggingface_hub")
        return True
    print(f"✅ hf found: {result.stdout.strip()}")
    return True


def login_hf():
    """Login HF CLI với hf auth login."""
    print("\n🔑 Logging in to Hugging Face...")
    print("⚠️  Nhập HF Token của bạn (từ https://huggingface.co/settings/tokens)")
    print("⚠️  Chọn token type: 'Write' hoặc 'Fine-grained (write)'")

    result = subprocess.run(
        ["hf", "auth", "login"],
        capture_output=False,
        text=True
    )

    return result.returncode == 0


def clone_space():
    """Clone Space từ HF."""
    if os.path.exists(SPACE_DIR):
        print(f"📂 Folder {SPACE_DIR} đã tồn tại, bỏ qua clone.")
        return True

    print(f"📥 Cloning Space from {SPACE_REPO}...")
    if not run_command(f"git clone {SPACE_REPO} {SPACE_DIR}"):
        print("❌ Failed to clone Space.")
        return False

    print("✅ Clone thành công!")
    return True


def copy_files():
    """Copy files vào Space folder."""
    print(f"\n📤 Copying files to {SPACE_DIR}/...")

    space_path = Path(SPACE_DIR)
    current_path = Path(".")

    # Copy files
    for file in FILES_TO_UPLOAD:
        src = current_path / file
        dst = space_path / file

        if src.exists():
            print(f"  📋 Copying {file}...")
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Copied {file}")
        else:
            print(f"  ❌ File {file} not found!")
            return False

    # Copy backend folder
    backend_src = current_path / BACKEND_DIR
    backend_dst = space_path / BACKEND_DIR

    if backend_src.exists():
        print(f"  📋 Copying {BACKEND_DIR}/...")
        if backend_dst.exists():
            import shutil
            shutil.rmtree(backend_dst)

        import shutil
        shutil.copytree(backend_src, backend_dst)
        print(f"  ✅ Copied {BACKEND_DIR}/")
    else:
        print(f"  ❌ Folder {BACKEND_DIR}/ not found!")
        return False

    print("✅ All files copied successfully!")
    return True


def commit_and_push():
    """Commit và push lên HF."""
    print(f"\n🔧 Committing changes to {SPACE_DIR}/...")

    if not run_command("git add .", cwd=SPACE_DIR):
        print("❌ Failed to add files.")
        return False

    if not run_command(f'git commit -m "Upload E-Commerce Product Intelligence Dashboard"', cwd=SPACE_DIR):
        print("❌ Failed to commit.")
        return False

    print("🚀 Pushing to Hugging Face...")
    if not run_command("git push", cwd=SPACE_DIR):
        print("❌ Failed to push.")
        return False

    print("\n✅✅✅ PUSH THÀNH CÔNG! ✅✅✅")
    print(f"\n📦 Space URL: https://{USERNAME}.hf.space/{SPACE_NAME}")
    print(f"📦 API Docs: https://{USERNAME}.hf.space/{SPACE_NAME}/docs")
    print(f"\n⏳ Đợi 2-5 phút Hugging Face build và chạy...")

    return True


def main():
    """Main function."""
    print("🚀🚀🚀 BẮT ĐẦU PUSH UPLOAD LÊN HUGGING FACE SPACE 🚀🚀🚀")
    print(f"📦 Space: {USERNAME}/{SPACE_NAME}")
    print(f"🔗 URL: {SPACE_REPO}")
    print()

    # Check hf CLI
    if not check_hf_cli():
        return False

    # Login
    if not login_hf():
        print("❌ Failed to login. Kiểm tra HF Token.")
        return False

    # Clone Space
    if not clone_space():
        return False

    # Copy files
    if not copy_files():
        return False

    # Commit & Push
    if not commit_and_push():
        return False

    print("\n🎉 HOÀN THÀNH! Bạn có thể truy cập API tại:")
    print(f"   https://{USERNAME}.hf.space/{SPACE_NAME}")
    print(f"   Swagger: https://{USERNAME}.hf.space/{SPACE_NAME}/docs")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)