import { Brain, MessagesSquare, Terminal, GitBranch, Gauge, Shield } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Deep project analysis",
    body: "Tech stack, architecture, key features and design decisions — distilled from the actual repository content.",
    tone: "primary",
  },
  {
    icon: MessagesSquare,
    title: "Interview questions",
    body: "Generate 3–25 tailored questions across beginner, intermediate or advanced — with hints and sample answers.",
    tone: "accent",
  },
  {
    icon: Terminal,
    title: "Step-by-step setup",
    body: "Get a clean install guide with commands, prerequisites, and warnings about common gotchas.",
    tone: "amber",
  },
  {
    icon: GitBranch,
    title: "LangGraph workflow",
    body: "A stateful graph orchestrates fetching, analysis and generation — composable and observable.",
    tone: "primary",
  },
  {
    icon: Gauge,
    title: "Fast endpoints",
    body: "Need only questions or only setup? Hit /questions-only or /setup-only for sub-second turnarounds.",
    tone: "accent",
  },
  {
    icon: Shield,
    title: "Your key, your data",
    body: "Bring your own Gemini API key. Requests never leave your server.",
    tone: "amber",
  },
];

const toneClass: Record<string, string> = {
  primary: "text-primary bg-primary/10 ring-primary/30",
  accent: "text-accent bg-accent/10 ring-accent/30",
  amber: "text-amber bg-amber/10 ring-amber/30",
};

export function Features() {
  return (
    <section id="features" className="relative py-28">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-2xl">
          <div className="font-mono text-xs uppercase tracking-widest text-primary">
            // features
          </div>
          <h2 className="mt-3 text-3xl md:text-5xl font-bold tracking-tight">
            Everything you need to <span className="text-gradient">grok a repo</span>.
          </h2>
          <p className="mt-4 text-muted-foreground">
            One API. Three deliverables. Built on a LangGraph agent that reads READMEs, source trees
            and metadata before it speaks.
          </p>
        </div>

        <div className="mt-14 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <div
              key={f.title}
              className="group relative rounded-xl border border-border bg-card p-6 shadow-card transition hover:border-primary/40 hover:-translate-y-0.5"
            >
              <div
                className={`inline-flex h-10 w-10 items-center justify-center rounded-lg ring-1 ${toneClass[f.tone]}`}
              >
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="mt-5 text-lg font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{f.body}</p>
              <div className="absolute inset-x-6 bottom-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent opacity-0 group-hover:opacity-100 transition" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
