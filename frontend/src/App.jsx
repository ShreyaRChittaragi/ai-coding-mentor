import { useState } from "react";
import ProblemPanel from "./components/ProblemPanel";
import CodeEditor from "./components/CodeEditor";
import FeedbackPanel from "./components/FeedbackPanel";
import InsightsPanel from "./components/InsightsPanel";
import "./App.css";

const USER_ID = "user_001";
const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [problemId, setProblemId] = useState("p001");
  const [code, setCode] = useState("def two_sum(nums, target):\n    pass");
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setFeedback(null);
    try {
      const params = new URLSearchParams({ user_id: USER_ID, problem_id: problemId, code });
      const res = await fetch(`${API_BASE}/get_feedback?${params}`, { method: "POST" });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setFeedback(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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
          <span className="user-badge">👤 {USER_ID}</span>
        </div>
      </header>

      <main className="app-layout">
        <aside className="left-panel">
          <ProblemPanel
            problemId={problemId}
            apiBase={API_BASE}
            userId={USER_ID}
            onProblemChange={(id, starterCode) => {
              setProblemId(id);
              if (starterCode) setCode(starterCode);
            }}
          />
          <InsightsPanel userId={USER_ID} apiBase={API_BASE} feedback={feedback} />
        </aside>

        <section className="center-panel">
          <div className="editor-header">
            <span className="editor-label">EDITOR</span>
            <span className="lang-badge">Python</span>
          </div>
          <CodeEditor code={code} onChange={setCode} />
          <div className="editor-footer">
            <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
              {loading ? (
                <><span className="spinner" /> Running...</>
              ) : (
                <><span>▶</span> Submit Code</>
              )}
            </button>
          </div>
        </section>

        <aside className="right-panel">
          <FeedbackPanel feedback={feedback} error={error} loading={loading} />
        </aside>
      </main>
    </div>
  );
}