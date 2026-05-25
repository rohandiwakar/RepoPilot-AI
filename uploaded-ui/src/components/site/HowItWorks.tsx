const steps = [
  {
    n: "01",
    title: "Paste a GitHub URL",
    body: "Public repo, any language. We fetch metadata, README and source tree via the GitHub API.",
  },
  {
    n: "02",
    title: "Agent reads the code",
    body: "A LangGraph workflow walks the repo and asks Gemini to analyze architecture & intent.",
  },
  {
    n: "03",
    title: "Generate deliverables",
    body: "Project breakdown, N interview questions at your chosen level, and a setup guide.",
  },
  {
    n: "04",
    title: "Ship to your UI",
    body: "Consume the JSON response in your app, docs site, onboarding flow or coding bootcamp.",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="relative py-28 border-t border-border/60">
      <div className="mx-auto max-w-7xl px-6">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <div className="max-w-xl">
            <div className="font-mono text-xs uppercase tracking-widest text-accent">
              // how it works
            </div>
            <h2 className="mt-3 text-3xl md:text-5xl font-bold tracking-tight">
              From URL to insight in <span className="text-gradient">four steps</span>.
            </h2>
          </div>
          <p className="text-muted-foreground max-w-md">
            The whole pipeline runs as a single LangGraph agent — observable, retriable and easy to
            extend with new nodes.
          </p>
        </div>

        <div className="mt-14 grid gap-px bg-border md:grid-cols-4 rounded-xl overflow-hidden border border-border">
          {steps.map((s) => (
            <div
              key={s.n}
              className="bg-card p-6 md:p-8 relative group hover:bg-card/60 transition"
            >
              <div className="font-mono text-xs text-primary">{s.n}</div>
              <h3 className="mt-4 font-semibold text-lg">{s.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{s.body}</p>
              <div className="absolute top-6 right-6 h-2 w-2 rounded-full bg-primary/40 group-hover:bg-primary transition" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
