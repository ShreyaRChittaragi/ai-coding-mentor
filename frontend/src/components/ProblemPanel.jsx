import { useState, useEffect } from "react";

export default function ProblemPanel({ problemId, apiBase, onProblemChange }) {
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
    } catch (err) {
      setError(err.message);
      setProblem(null);
    } finally {
      setLoading(false);
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
          {problem.difficulty && (
            <span className={`difficulty-badge ${difficultyClass}`}>
              {problem.difficulty}
            </span>
          )}
          <div className="problem-description">{problem.description}</div>
        </>
      )}
    </div>
  );
}
