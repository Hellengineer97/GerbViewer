from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread
import signal
import sys

ROOT = Path(__file__).resolve().parent

SERVERS = [
    (
        "API",
        [sys.executable, str(ROOT / "backend" / "gerbviewer_api.py")],
        ROOT / "backend",
    ),
    (
        "FRONT",
        [sys.executable, "-m", "http.server", "8000"],
        ROOT / "frontend",
    ),
]

processes = []


def stream_output(name, stream):
    for line in iter(stream.readline, b""):
        sys.stdout.write(f"[{name}] {line.decode('utf-8', 'replace')}".rstrip() + "\n")
    stream.close()


def shutdown(signum, frame):
    for proc, _, _ in processes:
        if proc.poll() is None:
            proc.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

for name, cmd, cwd in SERVERS:
    proc = Popen(cmd, cwd=cwd, stdout=PIPE, stderr=PIPE)
    Thread(target=stream_output, args=(name, proc.stdout), daemon=True).start()
    Thread(target=stream_output, args=(name, proc.stderr), daemon=True).start()
    processes.append((proc, name, cmd))

for proc, name, cmd in processes:
    proc.wait()
    if proc.returncode != 0:
        sys.stderr.write(f"[{name}] exited with code {proc.returncode}\n")
