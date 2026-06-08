import os
import json
import subprocess
from pathlib import Path


def get_changed_files():
    """Get changed files from GitHub event or git diff."""

    # Try GitHub event first (push)
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if event_path and os.path.exists(event_path):
        with open(event_path) as f:
            event = json.load(f)

        # Push event
        if 'commits' in event:
            changed_files = []
            for commit in event['commits']:
                changed_files.extend(commit.get('added', []))
                changed_files.extend(commit.get('modified', []))
                changed_files.extend(commit.get('removed', []))
            return changed_files

    # Fallback to git diff
    result = subprocess.run(
        ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD~1', 'HEAD'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')


def check_folders(changed_files):
    """Check which folders have changed files."""

    frontend_changed = False
    backend_changed = False
    data_changed = False

    for file in changed_files:
        if not file:
            continue

        print(f"📄 Checking: {file}")

        # Check frontend/
        if file.startswith('frontend/') or file.startswith('frontend/'):
            frontend_changed = True

        # Check backend/, app.py, requirements.txt, Dockerfile
        if file.startswith('backend/') or file == 'app.py' or file == 'requirements.txt' or file == 'Dockerfile':
            backend_changed = True

        # Check data/
        if file.startswith('data/'):
            data_changed = True

    return frontend_changed, backend_changed, data_changed


if __name__ == '__main__':
    changed_files = get_changed_files()

    print("📋 Changed files:")
    for file in changed_files:
        print(f"  - {file}")
    print()

    frontend, backend, data = check_folders(changed_files)

    print(f"frontend={frontend}")
    print(f"backend={backend}")
    print(f"data={data}")

    # Write to GITHUB_OUTPUT
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"frontend={frontend}\n")
        f.write(f"backend={backend}\n")
        f.write(f"data={data}\n")