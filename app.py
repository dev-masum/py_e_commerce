import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

projects = [
    BASE_DIR / "backend" / "app.py",
    BASE_DIR / "frontend" / "app.py",
    BASE_DIR / "admin" / "app.py",
]

for app in projects:
    print(f"Starting {app}")
    subprocess.Popen([sys.executable, str(app)])

print("All services started")
