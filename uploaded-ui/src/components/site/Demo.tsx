import { useState } from "react";
import { AlertCircle, ChevronRight, Loader2, Play } from "lucide-react";

type Tab = "analysis" | "questions" | "setup";
type Difficulty = "beginner" | "intermediate" | "advanced";

type AnalyzeResponse = {
  project_analysis?: {
    project_name?: string;
    description?: string;
    tech_stack?: string[];
    architecture_summary?: string;
    key_features?: string[];
  };
  interview_questions?: Array<{
    question?: string;
    category?: string;
    difficulty?: string;
    hint?: string | null;
    sample_answer?: string;
  }>;
  setup_instructions?: Array<{
    step_number?: number;
    title?: string;
    command?: string | null;
    description?: string;
    warning?: string | null;
  }>;
  prerequisites?: string[];
  potential_issues?: string[];
};

const API_BASE_URL = "http://127.0.0.1:8000";

export function Demo() {
  const [tab, setTab] = useState<Tab>("analysis");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState("");
  const [githubUrl, setGithubUrl] = useState("https://github.com/langchain-ai/langchain");
  const [difficulty, setDifficulty] = useState<Difficulty>("intermediate");
  const [numQuestions, setNumQuestions] = useState(10);

  const run = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          github_url: githubUrl,
          difficulty,
          num_questions: numQuestions,
        }),
      });

      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.detail || `Request failed with status ${response.status}`);
      }

      setData(payload);
      setTab("analysis");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to analyze this repository.");
    } finally {
      setLoading(false);
    }
  };

  const analysis = data?.project_analysis;
  const questions = data?.interview_questions ?? [];
  const setup = data?.setup_instructions ?? [];

  return (
    <section id="demo" className="relative py-28 border-t border-border/60">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-2xl">
          <div className="font-mono text-xs uppercase tracking-widest text-amber">
            // live analyzer
          </div>
          <h2 className="mt-3 text-3xl md:text-5xl font-bold tracking-tight">See it in action.</h2>
          <p className="mt-4 text-muted-foreground">
            Paste a public GitHub repository and the website will call the FastAPI analyzer running
            on your machine.
          </p>
        </div>

        <div className="mt-12 grid lg:grid-cols-[1fr_1.4fr] gap-6">
          <form
            onSubmit={(event) => {
              event.preventDefault();
              if (!loading) void run();
            }}
            className="rounded-2xl border border-border bg-card p-6 shadow-card h-fit"
          >
            <label className="font-mono text-xs text-muted-foreground">github_url</label>
            <input
              value={githubUrl}
              onChange={(event) => setGithubUrl(event.target.value)}
              placeholder="https://github.com/owner/repo"
              className="mt-1 w-full rounded-lg border border-border bg-background px-3 py-2.5 font-mono text-sm outline-none ring-primary/40 transition focus:ring-2"
              required
            />

            <label className="mt-5 block font-mono text-xs text-muted-foreground">difficulty</label>
            <div className="mt-1 flex gap-2">
              {(["beginner", "intermediate", "advanced"] as Difficulty[]).map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setDifficulty(d)}
                  className={`flex-1 rounded-lg border px-3 py-2 text-xs font-medium capitalize transition ${
                    difficulty === d
                      ? "border-primary/60 bg-primary/10 text-primary"
                      : "border-border text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>

            <label className="mt-5 block font-mono text-xs text-muted-foreground">
              num_questions: {numQuestions}
            </label>
            <input
              type="range"
              min={3}
              max={25}
              value={numQuestions}
              onChange={(event) => setNumQuestions(Number(event.target.value))}
              className="mt-2 w-full accent-[var(--primary)]"
            />

            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition shadow-glow disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Analyzing repo...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" /> Run analysis
                </>
              )}
            </button>

            <p className="mt-3 text-[11px] text-muted-foreground font-mono">POST /api/v1/analyze</p>
          </form>

          <div className="rounded-2xl border border-border bg-card shadow-card overflow-hidden relative scanline">
            <div className="flex border-b border-border bg-background/40">
              {(["analysis", "questions", "setup"] as Tab[]).map((t) => (
                <button
                  key={t}
                  onClick={() => setTab(t)}
                  className={`px-5 py-3 text-xs font-mono uppercase tracking-wider transition relative ${
                    tab === t ? "text-primary" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {t}
                  {tab === t && <span className="absolute inset-x-3 -bottom-px h-px bg-primary" />}
                </button>
              ))}
              <div className="ml-auto pr-4 flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
                {loading ? (
                  <>
                    <Loader2 className="h-3 w-3 animate-spin text-primary" /> streaming
                  </>
                ) : data ? (
                  <>
                    <span className="h-1.5 w-1.5 rounded-full bg-primary" /> done
                  </>
                ) : error ? (
                  <>
                    <span className="h-1.5 w-1.5 rounded-full bg-destructive" /> error
                  </>
                ) : (
                  <>
                    <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground/50" /> idle
                  </>
                )}
              </div>
            </div>

            <div className="p-6 min-h-[420px]">
              {loading ? (
                <LoadingState />
              ) : error ? (
                <ErrorState message={error} />
              ) : !data ? (
                <EmptyState />
              ) : tab === "analysis" ? (
                <AnalysisPanel
                  analysis={analysis}
                  prerequisites={data.prerequisites ?? []}
                  issues={data.potential_issues ?? []}
                />
              ) : tab === "questions" ? (
                <QuestionsPanel questions={questions} />
              ) : (
                <SetupPanel setup={setup} />
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function LoadingState() {
  return (
    <div className="space-y-3">
      {[80, 60, 90, 50, 75, 65].map((w, i) => (
        <div
          key={i}
          className="h-3 rounded bg-muted relative overflow-hidden"
          style={{ width: `${w}%` }}
        >
          <div className="absolute inset-0 animate-shimmer" />
        </div>
      ))}
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-destructive/40 bg-destructive/10 p-4 text-sm">
      <div className="flex items-start gap-3">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-destructive" />
        <div>
          <div className="font-semibold">Analysis failed</div>
          <p className="mt-1 text-muted-foreground">{message}</p>
        </div>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="grid min-h-[360px] place-items-center text-center">
      <div>
        <div className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
          ready
        </div>
        <p className="mt-2 max-w-sm text-sm text-muted-foreground">
          Enter a repository URL and run the analyzer to generate a real project report.
        </p>
      </div>
    </div>
  );
}

function AnalysisPanel({
  analysis,
  prerequisites,
  issues,
}: {
  analysis: AnalyzeResponse["project_analysis"];
  prerequisites: string[];
  issues: string[];
}) {
  return (
    <div className="space-y-5">
      <div>
        <div className="font-mono text-[11px] text-muted-foreground">project_name</div>
        <div className="mt-1 text-2xl font-bold">{analysis?.project_name || "Unknown project"}</div>
      </div>
      <p className="text-sm text-muted-foreground">{analysis?.description}</p>
      {analysis?.architecture_summary && (
        <p className="rounded-lg border border-border bg-background/40 p-3 text-sm text-muted-foreground">
          {analysis.architecture_summary}
        </p>
      )}
      <div>
        <div className="font-mono text-[11px] text-muted-foreground">tech_stack</div>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {(analysis?.tech_stack ?? []).map((t) => (
            <span
              key={t}
              className="rounded-md border border-primary/30 bg-primary/10 px-2 py-1 text-xs font-mono text-primary"
            >
              {t}
            </span>
          ))}
        </div>
      </div>
      <ResultList title="key_features" items={analysis?.key_features ?? []} />
      <div className="grid gap-3 md:grid-cols-2">
        <ResultList title="prerequisites" items={prerequisites} />
        <ResultList title="potential_issues" items={issues} />
      </div>
    </div>
  );
}

function QuestionsPanel({
  questions,
}: {
  questions: NonNullable<AnalyzeResponse["interview_questions"]>;
}) {
  return (
    <div className="space-y-3">
      {questions.map((q, i) => (
        <div
          key={`${q.question}-${i}`}
          className="rounded-lg border border-border bg-background/40 p-4 hover:border-primary/40 transition"
        >
          <div className="flex items-center gap-2 text-[10px] font-mono uppercase">
            <span className="text-muted-foreground">Q{i + 1}</span>
            {q.category && (
              <span className="rounded bg-accent/15 px-1.5 py-0.5 text-accent">{q.category}</span>
            )}
            {q.difficulty && (
              <span className="rounded bg-primary/15 px-1.5 py-0.5 text-primary">
                {q.difficulty}
              </span>
            )}
          </div>
          <p className="mt-2 text-sm">{q.question}</p>
          {q.hint && <p className="mt-2 text-xs text-muted-foreground">Hint: {q.hint}</p>}
          {q.sample_answer && (
            <p className="mt-3 text-xs leading-relaxed text-muted-foreground">{q.sample_answer}</p>
          )}
        </div>
      ))}
    </div>
  );
}

function SetupPanel({ setup }: { setup: NonNullable<AnalyzeResponse["setup_instructions"]> }) {
  return (
    <div className="space-y-2">
      {setup.map((s, i) => (
        <div
          key={`${s.title}-${i}`}
          className="rounded-lg border border-border bg-background/40 p-4"
        >
          <div className="flex items-center gap-3">
            <div className="h-7 w-7 grid place-items-center rounded-md bg-primary/15 text-primary font-mono text-xs">
              {s.step_number ?? i + 1}
            </div>
            <div className="font-medium text-sm">{s.title}</div>
          </div>
          {s.description && (
            <p className="mt-2 ml-10 text-xs text-muted-foreground">{s.description}</p>
          )}
          {s.command && (
            <pre className="mt-3 ml-10 rounded-md bg-background border border-border px-3 py-2 font-mono text-xs text-primary overflow-x-auto">
              $ {s.command}
            </pre>
          )}
          {s.warning && <p className="mt-2 ml-10 text-xs text-amber">{s.warning}</p>}
        </div>
      ))}
    </div>
  );
}

function ResultList({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;

  return (
    <div>
      <div className="font-mono text-[11px] text-muted-foreground">{title}</div>
      <ul className="mt-2 space-y-1.5 text-sm">
        {items.map((item) => (
          <li key={item} className="flex items-start gap-2">
            <ChevronRight className="h-4 w-4 text-primary mt-0.5 shrink-0" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
