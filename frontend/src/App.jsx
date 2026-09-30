import { useEffect, useState } from "react";
import { Activity, CarFront, CircleAlert, Gauge, Radio, ShieldCheck } from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [junctions, setJunctions] = useState([]);
  const [connection, setConnection] = useState("Connecting");

  useEffect(() => {
    fetch(`${API_URL}/api/junctions`)
      .then((response) => response.json())
      .then((data) => {
        setJunctions(data.items);
        setConnection("Demo data connected");
      })
      .catch(() => setConnection("Backend unavailable"));
  }, []);

  return (
    <main className="min-h-screen bg-[#08131d] text-slate-100">
      <div className="mx-auto max-w-[1440px] px-6 py-8 lg:px-10">
        <header className="mb-10 flex flex-wrap items-end justify-between gap-6 border-b border-slate-800 pb-7">
          <div>
            <div className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-cyan-300">
              <Radio size={14} /> Operations prototype
            </div>
            <h1 className="text-4xl font-semibold tracking-tight text-white lg:text-6xl">AI Traffic Intelligence Center</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">A Phase 1 control-room foundation for four independent junction agents. All values are clearly marked as synthetic demo data.</p>
          </div>
          <div className="flex items-center gap-3 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-xs text-emerald-200"><span className="h-2 w-2 rounded-full bg-emerald-300" />{connection}</div>
        </header>

        <section className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["Network state", "Awaiting data", Activity],
            ["Model status", "Not trained", Gauge],
            ["Video source", "Demo mode", CarFront],
            ["Safety mode", "Recommendations only", ShieldCheck],
          ].map(([label, value, Icon]) => <article key={label} className="rounded-xl border border-slate-800 bg-slate-900/70 p-5"><Icon className="mb-7 text-cyan-300" size={19} /><p className="text-xs uppercase tracking-widest text-slate-500">{label}</p><p className="mt-2 text-lg font-medium text-white">{value}</p></article>)}
        </section>

        <section>
          <div className="mb-4 flex items-center justify-between"><div><p className="text-xs font-semibold uppercase tracking-widest text-cyan-300">Junction network</p><h2 className="mt-2 text-2xl font-semibold text-white">Four-agent registry</h2></div><span className="rounded border border-amber-300/20 bg-amber-300/10 px-3 py-1.5 text-xs text-amber-200">DEMO DATA</span></div>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{junctions.map((junction) => <article key={junction.junction_id} className="rounded-xl border border-slate-800 bg-slate-900 p-5"><div className="mb-8 flex items-center justify-between"><span className="text-3xl font-semibold text-white">{junction.junction_id}</span><CircleAlert size={18} className="text-slate-600" /></div><p className="text-sm text-slate-300">{junction.name}</p><p className="mt-2 text-xs text-slate-500">{junction.status.replaceAll("_", " ")}</p></article>)}</div>
          {!junctions.length && <div className="rounded-xl border border-slate-800 bg-slate-900 p-8 text-sm text-slate-400">Start the FastAPI backend to load the junction registry.</div>}
        </section>
      </div>
    </main>
  );
}

export default App;
