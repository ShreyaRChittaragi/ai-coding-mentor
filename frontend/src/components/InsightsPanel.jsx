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
      const res = await fetch(`${apiBase}/user_profile/${userId}`);
      if (!res.ok) return;
      const data = await res.json();
      setProfile(data);
    } catch (_) {}
  };

  useEffect(() => { fetchProfile(); }, [userId]);

  // Refresh after new feedback comes in
  useEffect(() => {
    if (feedback) fetchProfile();
  }, [feedback]);

  const patterns = profile?.patterns ?? [];

  return (
    <div className="panel-card">
      <div className="panel-title">Insights</div>

      {patterns.length === 0 ? (
        <div className="no-insights">No patterns detected yet</div>
      ) : (
        patterns.slice(-5).map((p, i) => {
          const color = PATTERN_COLORS[p.pattern] || "#00e5a0";
          const confidence = Math.round((p.confidence ?? 0) * 100);
          return (
            <div key={i} className="pattern-item">
              <div className="pattern-header">
                <span className="pattern-name">{p.pattern?.replace("_", " ")}</span>
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
          ⚡ Latest: {feedback.pattern_detected.replace("_", " ")}
        </div>
      )}
    </div>
  );
}
