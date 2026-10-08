"""dbcopy as a Windows desktop app: the dashboard in a native window.

Run:   uv run --extra desktop python desktop.py
Build: uv run --extra desktop pyinstaller --noconfirm --onefile --windowed ^
           --name dbcopy --add-data "static;static" --collect-all webview desktop.py
"""

import os
import socket
import sys
import threading

# A --windowed exe has no console: stdout/stderr are None, and toolbox.py
# writes download progress to stderr. Give them somewhere to go.
sys.stdout = sys.stdout or open(os.devnull, "w")
sys.stderr = sys.stderr or open(os.devnull, "w")

import uvicorn
import webview

from app import app


def main():
    # Free port on loopback only: the desktop app is not a network server.
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_config=None))
    threading.Thread(target=server.run, daemon=True).start()
    while not server.started:
        threading.Event().wait(0.05)

    webview.create_window("dbcopy", f"http://127.0.0.1:{port}/", width=1200, height=850)
    webview.start()  # blocks until the window closes; daemon server dies with us


if __name__ == "__main__":
    main()
