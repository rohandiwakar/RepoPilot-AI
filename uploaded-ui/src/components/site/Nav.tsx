import { Github } from "lucide-react";

export function Nav() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-background/60 border-b border-border/60">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <a href="#top" className="flex items-center gap-2">
          <div className="relative h-7 w-7 rounded-md bg-primary/20 ring-1 ring-primary/40 grid place-items-center">
            <div className="h-2 w-2 rounded-full bg-primary animate-pulse-dot" />
          </div>
          <span className="font-mono text-sm font-semibold tracking-tight">
            RepoPilot<span className="text-primary"> AI</span>
          </span>
        </a>
        <nav className="hidden md:flex items-center gap-8 text-sm text-muted-foreground">
          <a href="#features" className="hover:text-foreground transition">
            Features
          </a>
          <a href="#how" className="hover:text-foreground transition">
            How it works
          </a>
          <a href="#demo" className="hover:text-foreground transition">
            Demo
          </a>
          <a href="#api" className="hover:text-foreground transition">
            API
          </a>
        </nav>
        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1.5 text-xs font-medium hover:border-primary/60 hover:text-primary transition"
        >
          <Github className="h-3.5 w-3.5" /> Star on GitHub
        </a>
      </div>
    </header>
  );
}
