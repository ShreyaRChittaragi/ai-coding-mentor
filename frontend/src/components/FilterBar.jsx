import { useState } from "react";

const TOPICS = ["arrays", "strings", "loops", "recursion", "sorting", "binary_search", "dictionaries", "stacks", "dynamic_programming"];
const DIFFICULTIES = ["easy", "medium", "hard"];

export default function FilterBar({ apiBase, onProblemChange }) {
  const [activeDifficulty, setActiveDifficulty] = useState(null);
  const [activeTopic, setActiveTopic] = useState("");
  const [genTopic, setGenTopic] = useState("arrays");
  const [genDifficulty, setGenDifficulty] = useState("easy");
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState(null);
  const [showGenPanel, setShowGenPanel] = useState(false);

  const filterByDifficulty = async (diff) => {
    if (activeDifficulty === diff) {
      setActiveDifficulty(null);
      return;
    }
    setActiveDifficulty(diff);
    try {
      const res = await fetch(`${apiBase}/problems/difficulty/${diff}`);
      if (!res.ok) return;
      const problems = await res.json();
      if (problems.length > 0) {
        const random = problems[Math.floor(Math.random() * problems.length)];
        onProblemChange(random.id, random.starter_code);
      }
    } catch (_) {}
  };

  const filterByTopic = async (topic) => {
    if (!topic) return;
    setActiveTopic(topic);
    try {
      const res = await fetch(`${apiBase}/problems/topic/${topic}`);
      if (!res.ok) return;
      const problems = await res.json();
      if (problems.length > 0) {
        const random = problems[Math.floor(Math.random() * problems.length)];
        onProblemChange(random.id, random.starter_code);
      }
    } catch (_) {}
  };

  const loadRandom = async () => {
    try {
      const res = await fetch(`${apiBase}/problems`);
      if (!res.ok) return;
      const problems = await res.json();
      if (problems.length > 0) {
        const random = problems[Math.floor(Math.random() * problems.length)];
        onProblemChange(random.id, random.starter_code);
      }
    } catch (_) {}
  };

  const generateProblem = async () => {
    setGenerating(true);
    setGenError(null);
    try {
      const res = await fetch(`${apiBase}/problems/generate/${genTopic}/${genDifficulty}`);
      if (!res.ok) throw new Error("Generation failed");
      const data = await res.json();
      const id = data.id || data.problem_id;
      onProblemChange(id, data.starter_code);
      setShowGenPanel(false);
    } catch (err) {
      setGenError("Failed to generate. Try again.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="filter-bar">
      <div className="filter-row">
        <div className="filter-group">
          {DIFFICULTIES.map(d => (
            <button
              key={d}
              className={`filter-btn difficulty-filter-${d} ${activeDifficulty === d ? "active" : ""}`}
              onClick={() => filterByDifficulty(d)}
            >
              {d}
            </button>
          ))}
        </div>

        <select
          className="topic-select"
          value={activeTopic}
          onChange={(e) => filterByTopic(e.target.value)}
        >
          <option value="">Topic...</option>
          {TOPICS.map(t => (
            <option key={t} value={t}>{t.replace("_", " ")}</option>
          ))}
        </select>

        <button className="random-btn" onClick={loadRandom}>🎲 Random</button>

        <button
          className={`generate-btn ${showGenPanel ? "active" : ""}`}
          onClick={() => setShowGenPanel(s => !s)}
        >
          ✨ Generate
        </button>
      </div>

      {showGenPanel && (
        <div className="gen-panel">
          <select
            className="topic-select"
            value={genTopic}
            onChange={(e) => setGenTopic(e.target.value)}
          >
            {TOPICS.map(t => (
              <option key={t} value={t}>{t.replace("_", " ")}</option>
            ))}
          </select>

          <select
            className="topic-select"
            value={genDifficulty}
            onChange={(e) => setGenDifficulty(e.target.value)}
          >
            {DIFFICULTIES.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          <button
            className="generate-submit-btn"
            onClick={generateProblem}
            disabled={generating}
          >
            {generating ? (
              <><span className="spinner" style={{ borderColor: "#0d0f14", borderTopColor: "transparent" }} /> Generating (3-5s)...</>
            ) : (
              "✨ Generate Problem"
            )}
          </button>

          {genError && <span className="gen-error">{genError}</span>}
        </div>
      )}
    </div>
  );
}
