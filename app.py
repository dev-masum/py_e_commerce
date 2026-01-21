import subprocess
import sys
import signal
from pathlib import Path

BASE_DIR = Path(__file__).parent

projects = [
    BASE_DIR / "backend" / "app.py",
    BASE_DIR / "frontend" / "app.py",
    BASE_DIR / "admin" / "app.py",
]

processes = []

def shutdown(signum=None, frame=None):
    print("\nShutting down all services...")
    for p in processes:
        if p.poll() is None:  # still running
            try:
                p.terminate()
            except Exception:
                pass
    sys.exit(0)

# Handle Ctrl+C and kill
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

for app in projects:
    print(f"Starting {app}")
    p = subprocess.Popen([sys.executable, str(app)])
    processes.append(p)

print("All services started. Press CTRL+C to stop.")

# Keep main process alive
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    shutdown()
