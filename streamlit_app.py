"""
Crowdlike Option B: Keep the existing React UI, run it inside Streamlit (iframe),
and optionally provide a Python backend (FastAPI) for data/services.

How it works
- Streamlit runs on http://localhost:8501
- A static server hosts the built React app (Vite dist) on http://localhost:<frontend_port>
- A FastAPI backend (optional) runs on http://localhost:<backend_port>

Notes
- This wrapper preserves UI fidelity (the React app stays intact).
- Streamlit is used as the “shell” (launch + orchestration + future Python tooling).
"""

from __future__ import annotations

import atexit
import os
import socket
import subprocess
import sys
from pathlib import Path
from typing import Optional

import streamlit as st


ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"  # Vite build output (npm run build)
DEFAULT_BACKEND_PORT = int(os.environ.get("CROWDLIKE_BACKEND_PORT", "8001"))
DEFAULT_FRONTEND_PORT = int(os.environ.get("CROWDLIKE_FRONTEND_PORT", "8502"))
START_BACKEND = os.environ.get("CROWDLIKE_START_BACKEND", "true").lower() in ("1", "true", "yes")


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) != 0


def _pick_port(preferred: int) -> int:
    if _port_is_free(preferred):
        return preferred
    # pick a random free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _start_process(cmd: list[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> subprocess.Popen:
    # Windows-friendly: use sys.executable where possible.
    return subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def _ensure_started():
    """Start backend + frontend servers once per Streamlit session."""
    if "crowdlike_started" in st.session_state:
        return

    # Backend (FastAPI via uvicorn)
    backend_port = _pick_port(DEFAULT_BACKEND_PORT)
    backend_url = f"http://127.0.0.1:{backend_port}"

    backend_proc = None
    if START_BACKEND:
        backend_proc = _start_process(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "backend_api:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(backend_port),
                "--log-level",
                "warning",
            ],
            cwd=ROOT,
            env={**os.environ},
        )

    # Frontend (static dist server)
    frontend_port = _pick_port(DEFAULT_FRONTEND_PORT)
    frontend_url = f"http://127.0.0.1:{frontend_port}"

    if not DIST_DIR.exists():
        st.session_state["crowdlike_started"] = True
        st.session_state["backend_url"] = backend_url
        st.session_state["frontend_url"] = None
        st.session_state["backend_proc"] = backend_proc
        st.session_state["frontend_proc"] = None
        return

    # python -m http.server serves dist/ as a static site
    frontend_proc = _start_process(
        [sys.executable, "-m", "http.server", str(frontend_port), "--bind", "127.0.0.1"],
        cwd=DIST_DIR,
        env={**os.environ},
    )

    st.session_state["crowdlike_started"] = True
    st.session_state["backend_url"] = backend_url
    st.session_state["frontend_url"] = frontend_url
    st.session_state["backend_proc"] = backend_proc
    st.session_state["frontend_proc"] = frontend_proc

    def _cleanup():
        for key in ("frontend_proc", "backend_proc"):
            p = st.session_state.get(key)
            try:
                if p and p.poll() is None:
                    p.terminate()
            except Exception:
                pass

    atexit.register(_cleanup)


def main():
    st.set_page_config(page_title="Crowdlike (Option B)", layout="wide")

    st.title("Crowdlike — Streamlit Wrapper (Option B)")
    st.caption("React UI preserved; Streamlit is the shell/orchestrator.")

    _ensure_started()

    backend_url = st.session_state.get("backend_url")
    frontend_url = st.session_state.get("frontend_url")

    with st.sidebar:
        st.header("Runtime")
        st.write("Backend (FastAPI):", backend_url if START_BACKEND else "disabled")
        st.write("Frontend (React):", frontend_url or "not built yet")
        st.divider()
        st.subheader("Build prerequisite")
        st.write("This wrapper expects a Vite build output at `./dist`.")
        st.code(
            "\n".join(
                [
                    "# 1) Install JS deps",
                    "npm install",
                    "",
                    "# 2) Point frontend to the Python backend (optional)",
                    "echo VITE_COINGECKO_API_URL=http://127.0.0.1:8001 > .env.local",
                    "",
                    "# 3) Build the React app",
                    "npm run build",
                    "",
                    "# 4) Run Streamlit",
                    "pip install -r requirements.txt",
                    "streamlit run streamlit_app.py",
                ]
            ),
            language="bash",
        )

    if not frontend_url:
        st.error("React build not found: `./dist` is missing.")
        st.markdown(
            """
**What to do**
1. Run `npm install`
2. (Optional) set `VITE_COINGECKO_API_URL` to the backend (see sidebar)
3. Run `npm run build`
4. Re-run `streamlit run streamlit_app.py`

If you prefer to run the React dev server instead of `dist`, you can keep using `npm run dev`
and then embed it by changing this wrapper (or just open it separately).
"""
        )
        return

    # Embed the React app
    st.components.v1.iframe(frontend_url, height=900, scrolling=True)

    # Optional: lightweight health check link
    if START_BACKEND:
        st.markdown(f"Backend health: `{backend_url}/health`")


if __name__ == "__main__":
    main()
