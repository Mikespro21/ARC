/* CROWDLIKE_INTERACTIVITY_V1
   - No layout changes
   - localStorage persistence
   - Agents: create/configure/details
   - Market: refresh + paper trades
   - Safety: sliders/toggle persist
   - Dashboard stats update + chart (Chart.js)
*/

const STORE_KEY = "crowdlike_state_v1";

const DEFAULT_STATE = {
  agents: [
    { id: "alpha", name: "Agent Alpha", strategy: "Aggressive", status: "active", cash: 2500, holdings: { BTC: 0.02, ETH: 0.15 }, pnlPct: 15.3 },
    { id: "beta",  name: "Agent Beta",  strategy: "Conservative", status: "active", cash: 2800, holdings: { BTC: 0.01, ETH: 0.10 }, pnlPct: 8.7 },
    { id: "gamma", name: "Agent Gamma", strategy: "Balanced", status: "active", cash: 2000, holdings: { BTC: 0.015, ETH: 0.12 }, pnlPct: 12.1 },
    { id: "delta", name: "Agent Delta", strategy: "Swing Trading", status: "paused", cash: 1950, holdings: { BTC: 0.0, ETH: 0.0 }, pnlPct: -2.3 }
  ],
  trades: [],
  market: {
    BTC: { price: 42150, change24h: 5.2 },
    ETH: { price: 2245,  change24h: 3.8 },
    SOL: { price: 98.5,  change24h: -1.2 },
    ADA: { price: 0.52,  change24h: 2.1 },
    DOT: { price: 7.35,  change24h: -0.8 },
    AVAX:{ price: 35.2,  change24h: 7.5 }
  },
  safety: { safetyExits: true, maxDailyLoss: 10, maxDrawdown: 15 },
  profile: { plan: "Pro Plan" }
};

function clone(x){ return JSON.parse(JSON.stringify(x)); }

function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    return raw ? JSON.parse(raw) : clone(DEFAULT_STATE);
  } catch {
    return clone(DEFAULT_STATE);
  }
}
function saveState() { localStorage.setItem(STORE_KEY, JSON.stringify(state)); }

function fmtUSD(n) {
  const v = Number(n || 0);
  return v.toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: v < 1 ? 4 : 0 });
}
function uid(prefix="id") {
  return prefix + "_" + Math.random().toString(16).slice(2) + "_" + Date.now().toString(16);
}

let state = loadState();

/* ---------- Modal + Toast ---------- */
let modalEl = null;
let toastEl = null;

function ensureModal() {
  if (modalEl) return;
  modalEl = document.createElement("div");
  modalEl.id = "modal-overlay";
  modalEl.className = "fixed inset-0 hidden items-center justify-center bg-black/40 z-[99999] p-4";
  modalEl.innerHTML = `
    <div class="w-full max-w-xl bg-white rounded-xl shadow-2xl overflow-hidden">
      <div class="flex items-center justify-between px-5 py-4 border-b border-gray-200">
        <h3 id="modal-title" class="text-lg font-bold">Modal</h3>
        <button id="modal-close" class="text-gray-500 hover:text-gray-700">✕</button>
      </div>
      <div id="modal-body" class="p-5"></div>
      <div id="modal-actions" class="px-5 py-4 border-t border-gray-200 flex justify-end gap-3"></div>
    </div>
  `;
  document.body.appendChild(modalEl);
  modalEl.querySelector("#modal-close").addEventListener("click", closeModal);
  modalEl.addEventListener("click", (e) => { if (e.target === modalEl) closeModal(); });
}
function openModal(title, bodyHtml, actions=[]) {
  ensureModal();
  modalEl.querySelector("#modal-title").textContent = title;
  modalEl.querySelector("#modal-body").innerHTML = bodyHtml;
  const actionsEl = modalEl.querySelector("#modal-actions");
  actionsEl.innerHTML = "";
  actions.forEach(a => {
    const b = document.createElement("button");
# ------------------------------------------------------------
# RUN THIS IN GIT BASH (Windows) FROM YOUR LOCAL MACHINE
# It will:
#  1) Ensure Streamlit Cloud entrypoint is app.py
#  2) Add Microsoft Clarity (heatmap) injection for Streamlit
#  3) Add a client-side interactivity layer (agents/market/safety/profile)
#  4) Commit + push to https://github.com/Mikespro21/ARC
# ------------------------------------------------------------

set -euo pipefail

# 0) Go to your local repo (adjust if needed)
cd /c/Users/mange/Downloads/ARC

git pull

# 1) Ensure Streamlit Cloud expects app.py and it exists at repo root
if [ -f "streamlit_app.py" ] && [ ! -f "app.py" ]; then
  git mv streamlit_app.py app.py
fi

# If you only have a different file name (e.g., main.py), rename it to app.py:
# (uncomment and adjust)
# git mv main.py app.py

# 2) Make sure requirements.txt exists and includes streamlit
if [ ! -f "requirements.txt" ]; then
  cat > requirements.txt <<'EOF'
streamlit>=1.30
