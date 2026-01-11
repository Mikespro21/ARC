from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DATA_DIR = Path(".crowdlike_data")
USERS_DIR = DATA_DIR / "users"
ACTIVE_FILE = DATA_DIR / "active_user.json"


def _ensure_dirs() -> None:
    USERS_DIR.mkdir(parents=True, exist_ok=True)


def safe_username(name: str) -> str:
    """Normalize a username to a safe, file-friendly id.

    Rules (demo-safe):
    - lowercased
    - spaces -> underscore
    - allowed: a-z, 0-9, underscore
    - 3..20 chars
    """
    raw = (name or "").strip().lower()
    raw = re.sub(r"\s+", "_", raw)
    raw = re.sub(r"[^a-z0-9_]", "", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    if len(raw) < 3:
        return "member"
    return raw[:20]


def _user_path(user_id: str) -> Path:
    _ensure_dirs()
    return USERS_DIR / f"{safe_username(user_id)}.json"


def load_user(user_id: str) -> Optional[Dict[str, Any]]:
    try:
        p = _user_path(user_id)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_user(user_id: str, data: Dict[str, Any]) -> None:
    try:
        p = _user_path(user_id)
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        # Fail silently (local persistence is best-effort)
        pass


def load_active_user() -> Optional[str]:
    try:
        if not ACTIVE_FILE.exists():
            return None
        data = json.loads(ACTIVE_FILE.read_text(encoding="utf-8"))
        u = (data.get("user_id") or "").strip()
        return u or None
    except Exception:
        return None


def save_active_user(user_id: Optional[str]) -> None:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not user_id:
            if ACTIVE_FILE.exists():
                ACTIVE_FILE.unlink()
            return
        ACTIVE_FILE.write_text(json.dumps({"user_id": safe_username(user_id)}), encoding="utf-8")
    except Exception:
        pass


def delete_user(user_id: str) -> bool:
    try:
        p = _user_path(user_id)
        if p.exists():
            p.unlink()
        # If they were active, clear
        active = load_active_user()
        if active and safe_username(active) == safe_username(user_id):
            save_active_user(None)
        return True
    except Exception:
        return False
