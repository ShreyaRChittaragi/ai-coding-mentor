import { useState, useEffect, useRef } from "react";
import ProblemPanel from "./components/ProblemPanel";
import CodeEditor from "./components/CodeEditor";
import FeedbackPanel from "./components/FeedbackPanel";
import InsightsPanel from "./components/InsightsPanel";
import PatternChart from "./components/PatternChart";
import FilterBar from "./components/FilterBar";
import "./App.css";

const USER_ID = "test_user";
const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function App() {
  const [problemId, setProblemId] = useState("p001");
  const [code, setCode] = useState("def two_sum(nums, target):\n    pass");
  const [feedback, setFeedback] = useState(null);
  const [feedbackMode, setFeedbackMode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hintLoading, setHintLoading] = useState(false);
  const [error, setError] = useState(null);
  const [submitCount, setSubmitCount] = useState(0);
  const [attemptNumber, setAttemptNumber] = useState(1);
  const [editCount, setEditCount] = useState(0);
  const [problemStartTime, setProblemStartTime] = useState(Date.now());

  const handleProblemChange = (id, starterCode) => {
    setProblemId(id);
    if (starterCode) setCode(starterCode);
    setFeedback(null);
    setFeedbackMode(null);
    setAttemptNumber(1);
    setEditCount(0);
    setProblemStartTime(Date.now());
  };

  const handleCodeChange = (val) => {
    setCode(val);
    setEditCount(c => c + 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setFeedback(null);
    const timeTaken = Math.round((Date.now() - problemStartTime) / 1000);
    try {
      const submitRes = await fetch(`${API_BASE}/submit_code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: USER_ID,
          problem_id: problemId,
          code,
          language: "python",
          time_taken: timeTaken,
          attempt_number: attemptNumber,
          code_edit_count: editCount,
        }),
      });
      const submitData = submitRes.ok ? await submitRes.json() : null;

      const params = new URLSearchParams({ user_id: USER_ID, problem_id: problemId, code });
      const feedbackRes = await fetch(`${API_BASE}/get_feedback?${params}`, { method: "POST" });
      if (!feedbackRes.ok) throw new Error(`Server error: ${feedbackRes.status}`);
      const feedbackData = await feedbackRes.json();

      if (!feedbackData.eval_result && submitData?.eval_result) {
        feedbackData.eval_result = submitData.eval_result;
      }

      setFeedback(feedbackData);
      setFeedbackMode("submit");
      setSubmitCount(c => c + 1);
      setAttemptNumber(a => a + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGetHint = async () => {
    setHintLoading(true);
    try {
      const params = new URLSearchParams({ user_id: USER_ID, problem_id: problemId, code });
      const res = await fetch(`${API_BASE}/get_feedback?${params}`, { method: "POST" });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setFeedback(data);
      setFeedbackMode("hint");
    } catch (err) {
      setError(err.message);
    } finally {
      setHintLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <span className="logo">⟨/⟩</span>
          <span className="app-title">AI Coding Mentor</span>
        </div>
        <div className="header-right">
          {submitCount > 0 && (
            <span className="submit-count-badge">
              {submitCount} submit{submitCount !== 1 ? "s" : ""}
            </span>
          )}
          <span className="attempt-badge">attempt #{attemptNumber}</span>
          <span className="user-badge">👤 {USER_ID}</span>
        </div>
      </header>

      <main className="app-layout">
        <aside className="left-panel">
          <ProblemPanel
            problemId={problemId}
            apiBase={API_BASE}
            userId={USER_ID}
            onProblemChange={handleProblemChange}
          />
          <InsightsPanel userId={USER_ID} apiBase={API_BASE} feedback={feedback} />
          <PatternChart userId={USER_ID} apiBase={API_BASE} />
        </aside>

        <section className="center-panel">
          <FilterBar apiBase={API_BASE} onProblemChange={handleProblemChange} />
          <div className="editor-header">
            <span className="editor-label">EDITOR</span>
            <div className="editor-header-right">
              <span className="edit-chip">✏ {editCount} edits</span>
              <span className="problem-id-chip">{problemId}</span>
              <span className="lang-badge">Python</span>
            </div>
          </div>
          <CodeEditor code={code} onChange={handleCodeChange} />
          <div className="editor-footer">
            <div className="footer-left">
              {feedback?.eval_result && feedbackMode === "submit" && (
                <span className={`footer-status ${feedback.eval_result.all_passed ? "status-pass" : "status-fail"}`}>
                  {feedback.eval_result.all_passed ? "✓" : "✗"} {feedback.eval_result.passed_count}/{feedback.eval_result.total} tests
                </span>
              )}
            </div>
            <div className="footer-right">
              <button className="hint-btn" onClick={handleGetHint} disabled={hintLoading || loading}>
                {hintLoading ? <><span className="spinner" style={{ borderColor: "#fff", borderTopColor: "transparent" }} /> Thinking...</> : "💡 Get Hint"}
              </button>
              <button className="submit-btn" onClick={handleSubmit} disabled={loading || hintLoading}>
                {loading ? (
                  <><span className="spinner" /> Running...</>
                ) : (
                  <><span>▶</span> Submit Code</>
                )}
              </button>
            </div>
          </div>
        </section>

        <aside className="right-panel">
          <FeedbackPanel feedback={feedback} error={error} loading={loading || hintLoading} mode={feedbackMode} />
        </aside>
      </main>
    </div>
  );
}
