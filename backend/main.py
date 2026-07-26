import os
import socket
import sys
from pathlib import Path

import uvicorn

# Make the backend root importable for the project package layout
BACKEND_ROOT = Path(__file__).resolve().parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def find_available_port(preferred_port: int) -> int:
    for port in [preferred_port, *range(preferred_port + 1, preferred_port + 21)]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available port found in range")


if __name__ == "__main__":
    preferred_port = int(os.getenv("PORT", "8000"))
    port = find_available_port(preferred_port)
    print(f"Starting backend on port {port}")
    uvicorn.run("src.utils.fraud_dashboard.main:app", host="0.0.0.0", port=port, reload=False)
