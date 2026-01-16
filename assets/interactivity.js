/* CROWDLIKE_INTERACTIVITY_V1 */
(function () {
  const STORE="crowdlike_state_v1";
  const COINS={BTC:"bitcoin",ETH:"ethereum",SOL:"solana",ADA:"cardano",DOT:"polkadot",AVAX:"avalanche-2"};

  function load(){ try { return JSON.parse(localStorage.getItem(STORE)||"{}"); } catch { return {}; } }
  function save(s){ localStorage.setItem(STORE, JSON.stringify(s)); }
  function slug(s){ return (s||"").trim().toLowerCase().replace(/\s+/g,"_").replace(/[^a-z0-9_]/g,""); }

  let st=load();
  st.trades=Number.isFinite(st.trades)?st.trades:0;
  st.agents=Array.isArray(st.agents)?st.agents:[];
  st.safety=(st.safety&&typeof st.safety==="object")?st.safety:{};
  save(st);

  function toast(msg){
    let el=document.getElementById("__toast");
    if(!el){
      el=document.createElement("div"); el.id="__toast";
      el.style.position="fixed"; el.style.right="16px"; el.style.bottom="16px";
      el.style.zIndex="999999"; document.body.appendChild(el);
    }
    el.innerHTML='<div style="background:#111827;color:#fff;padding:10px 12px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.25);font-size:13px;max-width:360px;">'+msg+'</div>';
    setTimeout(()=>{ el.innerHTML=""; },2200);
  }

  function ev(name){ try{ window.clarity && window.clarity("event", name); } catch {} }

  function setActiveTrades(n){
    const cards=[...document.querySelectorAll("#page-dashboard .bg-white")];
    const c=cards.find(x=>(x.textContent||"").includes("Active Trades"));
    const h3=c?c.querySelector("h3"):null;
    if(h3) h3.textContent=String(n);
  }

  function findBtn(rootSel, contains){
    const root=rootSel?document.querySelector(rootSel):document;
    if(!root) return null;
    return [...root.querySelectorAll("button")]
      .find(b=>(b.textContent||"").toLowerCase().includes(contains.toLowerCase())) || null;
  }

  function bindOnce(el,key,fn){
    if(!el) return;
    if(el.dataset[key]==="1") return;
    el.dataset[key]="1";
    el.addEventListener("click", fn);
  }

    const safety=document.getElementById("page-safety");
    if(safety){
      [...safety.querySelectorAll('input[type="range"]')].forEach((rng,i)=>{
        const k="range_"+i;
        if(st.safety[k]!=null) rng.value=String(st.safety[k]);
        rng.addEventListener("input",()=>{ st.safety[k]=Number(rng.value); save(st); ev("safety_slider"); });
      });
    }
    document.querySelectorAll("button").forEach(btn=>{
      bindOnce(btn,"boundGeneric",()=>{
        const t=(btn.textContent||"").trim();
        if(!t) return;
        toast(t+" clicked");
        ev("click_"+slug(t));
      });
    });

    toast("Interactivity loaded");
  }

  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
