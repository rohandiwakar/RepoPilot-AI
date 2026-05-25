const endpoints = [
  {
    method: "POST",
    path: "/api/v1/analyze",
    desc: "Full analysis: project breakdown + questions + setup",
    tone: "primary",
  },
  {
    method: "POST",
    path: "/api/v1/analyze/questions-only",
    desc: "Generate only interview questions (faster)",
    tone: "accent",
  },
  {
    method: "POST",
    path: "/api/v1/analyze/setup-only",
    desc: "Generate only setup instructions (faster)",
    tone: "amber",
  },
  { method: "GET", path: "/api/v1/health", desc: "Service health check", tone: "primary" },
];

const toneBg: Record<string, string> = {
  primary: "text-primary bg-primary/10 ring-primary/30",
  accent: "text-accent bg-accent/10 ring-accent/30",
  amber: "text-amber bg-amber/10 ring-amber/30",
};

const sampleCurl = `curl -X POST http://localhost:8000/api/v1/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "github_url": "https://github.com/langchain-ai/langchain",
    "difficulty": "intermediate",
    "num_questions": 10
  }'`;

export function Api() {
  return (
    <section id="api" className="relative py-28 border-t border-border/60">
      <div className="mx-auto max-w-7xl px-6 grid lg:grid-cols-2 gap-12 items-start">
        <div>
          <div className="font-mono text-xs uppercase tracking-widest text-primary">
            // developer api
          </div>
          <h2 className="mt-3 text-3xl md:text-5xl font-bold tracking-tight">
            Built for builders.
          </h2>
          <p className="mt-4 text-muted-foreground">
            A small, focused FastAPI surface. Four endpoints, typed Pydantic schemas, OpenAPI docs
            at <span className="font-mono text-foreground">/docs</span>.
          </p>

          <div className="mt-8 space-y-2">
            {endpoints.map((e) => (
              <div
                key={e.path}
                className="flex items-center gap-3 rounded-lg border border-border bg-card p-3 hover:border-primary/40 transition"
              >
                <span
                  className={`shrink-0 rounded-md px-2 py-1 ring-1 text-[10px] font-mono font-bold ${toneBg[e.tone]}`}
                >
                  {e.method}
                </span>
                <code className="text-sm font-mono">{e.path}</code>
                <span className="ml-auto hidden sm:block text-xs text-muted-foreground">
                  {e.desc}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-card shadow-card overflow-hidden">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3 bg-background/40">
            <div className="font-mono text-xs text-muted-foreground">terminal</div>
            <div className="ml-auto font-mono text-[10px] text-primary">~/projects/repopilot-ai</div>
          </div>
          <pre className="p-5 text-xs font-mono leading-relaxed overflow-x-auto text-foreground">
            {sampleCurl}
          </pre>
          <div className="border-t border-border bg-background/40 px-5 py-3 font-mono text-[11px] text-muted-foreground">
            ↳ Response: <span className="text-primary">200 OK</span> · ~3.4s · 12kb JSON
          </div>
        </div>
      </div>
    </section>
  );
}
