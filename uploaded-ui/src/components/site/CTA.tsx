import { ArrowRight, Github } from "lucide-react";

export function CTA() {
  return (
    <section className="relative py-28">
      <div className="mx-auto max-w-5xl px-6">
        <div className="relative rounded-3xl border border-border bg-card overflow-hidden shadow-card">
          <div className="absolute inset-0 bg-grid opacity-50" />
          <div className="absolute -top-20 left-1/2 -translate-x-1/2 h-60 w-[120%] bg-primary/15 blur-3xl" />
          <div className="relative px-8 md:px-16 py-16 text-center">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
              Stop guessing. <span className="text-gradient">Start shipping.</span>
            </h2>
            <p className="mt-4 text-muted-foreground max-w-xl mx-auto">
              Drop RepoPilot AI into your onboarding, coding bootcamp, or recruiting workflow today.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <a
                href="#demo"
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground shadow-glow hover:opacity-90 transition"
              >
                Try the live demo <ArrowRight className="h-4 w-4" />
              </a>
              <a
                href="#api"
                className="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-5 py-3 text-sm font-medium hover:border-primary/40 transition"
              >
                <Github className="h-4 w-4" /> View on GitHub
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
