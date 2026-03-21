import { useState, useEffect } from "react";

export default function ProblemPanel({ problemId, apiBase, onProblemChange, userId }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(false);
  const [nextLoading, setNextLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputId, setInputId] = useState(problemId);
  const [nextReason, setNextReason] = useState(null);

  const loadProblem = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/get_problem/${id}`);
      if (!res.ok) throw new Error("Problem not found");
      const data = await res.json();
      setProblem(data);
      setInputId(id);
      onProblemChange(id, data.starter_code);
    } catch (err) {
      setError(err.message);
      setProblem(null);
    } finally {
      setLoading(false);
    }
  };

  const loadNextProblem = async () => {
    setNextLoading(true);
    setNextReason(null);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/next_problem/${userId}`);
      if (!res.ok) throw new Error("Could not fetch next problem");
      const data = await res.json();
      const nextId = data.next_problem?.id || data.problem_id || data.id;
      if (data.reason) setNextReason(data.reason);
      await loadProblem(nextId);
    } catch (err) {
      setError(err.message);
    } finally {
      setNextLoading(false);
    }
  };

  useEffect(() => { loadProblem(problemId); }, []);

  const difficultyClass = problem?.difficulty
    ? `difficulty-${problem.difficulty.toLowerCase()}`
    : "difficulty-easy";

  return (
    <div className="panel-card" style={{ flex: 1 }}>
      <div className="panel-title">Problem</div>

      <div className="problem-selector">
        <input
          className="problem-input"
          value={inputId}
          onChange={(e) => setInputId(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && loadProblem(inputId)}
          placeholder="problem_id"
        />
        <button className="load-btn" onClick={() => loadProblem(inputId)}>
          Load
        </button>
      </div>

      {loading && <div className="problem-loading">Loading...</div>}
      {error && <div className="problem-error">⚠ {error}</div>}

      {problem && !loading && (
        <>
          <div className="problem-title">{problem.title}</div>
          <div className="problem-meta">
            {problem.difficulty && (
              <span className={`difficulty-badge ${difficultyClass}`}>
                {problem.difficulty}
              </span>
            )}
            {problem.topic && (
              <span className="topic-badge">{problem.topic}</span>
            )}
          </div>
          <div className="problem-description">{problem.description}</div>
        </>
      )}

      {nextReason && (
        <div className="next-reason">
          <span className="next-reason-label">Why this problem?</span>
          {nextReason}
        </div>
      )}

      <button
        className="next-btn"
        onClick={loadNextProblem}
        disabled={nextLoading}
        style={{ marginTop: "12px" }}
      >
        {nextLoading ? (
          <><span className="spinner" style={{ borderColor: "#fff", borderTopColor: "transparent" }} /> Finding...</>
        ) : (
          <>⚡ Next Problem</>
        )}
      </button>
    </div>
  );
}
