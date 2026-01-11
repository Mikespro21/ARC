from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple
import time

from .limits import allow


def _day_key() -> str:
    # Uses server local time; good enough for demo.
    return time.strftime("%Y-%m-%d")


@dataclass
class PaymentPolicy:
    """Simple safety rails for on-chain USDC payments (demo).

    Stored in user['policy'] and enforced in checkout before presenting a payment action.
    """

    max_per_tx_usdc: float = 0.10
    daily_cap_usdc: float = 0.50
    cooldown_s: int = 15

    @classmethod
    def from_user(cls, user: Dict[str, Any]) -> "PaymentPolicy":
        p = user.get("policy") if isinstance(user.get("policy"), dict) else {}
        def _f(key: str, default: float) -> float:
            try:
                return float(p.get(key, default))
            except Exception:
                return default
        def _i(key: str, default: int) -> int:
            try:
                return int(p.get(key, default))
            except Exception:
                return default
        return cls(
            max_per_tx_usdc=max(0.0, _f("max_per_tx_usdc", cls.max_per_tx_usdc)),
            daily_cap_usdc=max(0.0, _f("daily_cap_usdc", cls.daily_cap_usdc)),
            cooldown_s=max(0, _i("cooldown_s", cls.cooldown_s)),
        )

    def authorize_payment(self, user: Dict[str, Any], amount_usdc: float, commit: bool = True) -> Tuple[bool, str]:
        """Return (ok, message). If commit=True, updates counters/totals in user state."""
        try:
            amt = float(amount_usdc or 0.0)
        except Exception:
            return False, "Invalid amount."
        if amt <= 0:
            return False, "Amount must be > 0."

        if self.max_per_tx_usdc > 0 and amt > self.max_per_tx_usdc + 1e-9:
            return False, f"Policy: amount exceeds max per tx (${self.max_per_tx_usdc:.2f})."

        # Daily cap
        limits = user.setdefault("limits", {})
        day = _day_key()
        total_key = f"pay.usdc.total.{day}"
        try:
            total = float(limits.get(total_key, 0.0) or 0.0)
        except Exception:
            total = 0.0
        if self.daily_cap_usdc > 0 and (total + amt) > self.daily_cap_usdc + 1e-9:
            return False, f"Policy: daily cap reached (${self.daily_cap_usdc:.2f})."

        # Cooldown gate (prevents spam / repeated clicks)
        if commit:
            ok, why = allow(user, key="pay.usdc", cooldown_s=self.cooldown_s, daily_max=None)
            if not ok:
                return False, f"Policy: {why or 'cooldown active'}"

            limits[total_key] = round(total + amt, 6)

        return True, "Allowed."
