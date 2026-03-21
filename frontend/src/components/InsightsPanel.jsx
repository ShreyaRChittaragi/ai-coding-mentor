import { useState, useEffect } from "react";

const PATTERN_COLORS = {
  overthinking:      "#7c6ff7",
  guessing:          "#f59e0b",
  concept_gap:       "#f87171",
  boundary_weakness: "#38bdf8",
  rushing:           "#fb923c",
};

export default function InsightsPanel({ userId, apiBase, feedback }) {
  const [profile, setProfile] = useState(null);

  const fetchProfile = async () => {
    try {
      const res = await fetch(`${apiBase}/memory/recall/${userId}`);
      if (!res.ok) return;
      const data = await res.json();
      setProfile(data);
    } catch (_) {}
  };

  useEffect(() => { fetchProfile(); }, [userId]);

  useEffect(() => {
    if (feedback) fetchProfile();
  }, [feedback]);

  const patterns = profile?.memory?.patterns ?? profile?.patterns ?? [];
  const totalSessions = profile?.memory?.total_sessions ?? profile?.total_sessions ?? 0;

  // Deduplicate patterns — show unique with highest confidence
  const uniquePatterns = Object.values(
    patterns.reduce((acc, p) => {
      if (!acc[p.pattern] || p.confidence > acc[p.pattern].confidence) {
        acc[p.pattern] = p;
      }
      return acc;
    }, {})
  ).sort((a, b) => b.confidence - a.confidence);

  return (
    <div className="panel-card">
      <div className="insights-header">
        <div className="panel-title" style={{ margin: 0 }}>Insights</div>
        {totalSessions > 0 && (
          <span className="session-count">{totalSessions} session{totalSessions !== 1 ? "s" : ""}</span>
        )}
      </div>

      {uniquePatterns.length === 0 ? (
        <div className="no-insights">No patterns detected yet</div>
      ) : (
        uniquePatterns.map((p, i) => {
          const color = PATTERN_COLORS[p.pattern] || "#00e5a0";
          const confidence = Math.round((p.confidence ?? 0) * 100);
          return (
            <div key={i} className="pattern-item">
              <div className="pattern-header">
                <span className="pattern-name">{p.pattern?.replace(/_/g, " ")}</span>
                <span className="pattern-score">{confidence}%</span>
              </div>
              <div className="pattern-bar">
                <div
                  className="pattern-fill"
                  style={{ width: `${confidence}%`, background: color }}
                />
              </div>
            </div>
          );
        })
      )}

      {feedback?.pattern_detected && (
        <div className="pattern-detected">
          ⚡ Latest: {feedback.pattern_detected.replace(/_/g, " ")}
        </div>
      )}
    </div>
  );
}
