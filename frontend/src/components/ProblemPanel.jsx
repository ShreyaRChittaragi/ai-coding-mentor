import { useState, useEffect } from "react";

export default function ProblemPanel({ problemId, apiBase, onProblemChange, onCodeChange }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputId, setInputId] = useState(problemId);

  const loadProblem = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/get_problem/${id}`);
      if (!res.ok) throw new Error("Problem not found");
      const data = await res.json();
      setProblem(data);
      onProblemChange(id);
      // Pre-fill editor with starter code
      if (data.starter_code && onCodeChange) {
        onCodeChange(data.starter_code);
      }
    } catch (err) {
      setError(err.message);
      setProblem(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadProblem(problemId); }, []);

  const diffClass = problem?.difficulty
    ? `difficulty-${problem.difficulty.toLowerCase()}`
    : "difficulty-easy";

  return (
    <div className="panel-section" style={{ flex: 1, overflowY: "auto" }}>
      <div className="panel-label">
        <span className="panel-label-dot" />
        Problem
      </div>

      <div className="problem-selector">
        <input
          className="problem-input"
          value={inputId}
          onChange={(e) => setInputId(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && loadProblem(inputId)}
          placeholder="e.g. p001"
        />
        <button className="load-btn" onClick={() => loadProblem(inputId)}>
          Load
        </button>
      </div>

      {loading && (
        <div className="problem-loading">
          <span className="spinner" style={{ borderColor: "var(--text-dim)", borderTopColor: "transparent" }} />
          Loading...
        </div>
      )}

      {error && <div className="problem-error">⚠ {error}</div>}

      {problem && !loading && (
        <>
          <div className="problem-title">{problem.title}</div>
          {problem.difficulty && (
            <span className={`difficulty-badge ${diffClass}`}>
              {problem.difficulty}
            </span>
          )}
          <div className="problem-description">{problem.description}</div>

          {problem.examples?.length > 0 && (
            <div style={{ marginTop: 14 }}>
              <div className="section-label" style={{ marginBottom: 6 }}>Example</div>
              {problem.examples.slice(0, 1).map((ex, i) => (
                <div key={i} style={{
                  background: "var(--bg4)",
                  border: "1px solid var(--border)",
                  borderRadius: "var(--radius-sm)",
                  padding: "8px 10px",
                  fontFamily: "var(--font-mono)",
                  fontSize: 10.5,
                  color: "var(--text-mid)",
                  lineHeight: 1.7
                }}>
                  <div><span style={{ color: "var(--text-dim)" }}>Input: </span>{ex.input}</div>
                  <div><span style={{ color: "var(--text-dim)" }}>Output: </span>{ex.output}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}