import { useState, useEffect } from "react";

const PATTERN_COLORS = {
  overthinking:      "#818cf8",
  guessing:          "#fbbf24",
  concept_gap:       "#fb7185",
  boundary_weakness: "#38bdf8",
  rushing:           "#fb923c",
  gives_up_early:    "#a78bfa",
};

const PATTERN_LABELS = {
  overthinking:      "Overthinking",
  guessing:          "Guessing",
  concept_gap:       "Concept Gap",
  boundary_weakness: "Boundary Weakness",
  rushing:           "Rushing",
  gives_up_early:    "Gives Up Early",
};

export default function InsightsPanel({ userId, apiBase, feedback }) {
  const [profile, setProfile] = useState(null);
  const [userProfile, setUserProfile] = useState(null);

  const fetchProfile = async () => {
    try {
      const res = await fetch(`${apiBase}/memory/recall/${userId}`);
      if (!res.ok) return;
      const data = await res.json();
      setProfile(data);
    } catch (_) {}
  };

  const fetchUserProfile = async () => {
    try {
      const res = await fetch(`${apiBase}/user_profile/${userId}`);
      if (!res.ok) return;
      const data = await res.json();
      setUserProfile(data);
    } catch (_) {}
  };

  useEffect(() => {
    fetchProfile();
    fetchUserProfile();
  }, [userId]);

  useEffect(() => {
    if (feedback) {
      fetchProfile();
      fetchUserProfile();
    }
  }, [feedback]);

  const rawPatterns = profile?.memory?.patterns ?? profile?.patterns ?? [];
  const deduped = Object.values(
    rawPatterns.reduce((acc, p) => {
      const key = p.pattern;
      if (!acc[key] || p.confidence > acc[key].confidence) acc[key] = p;
      return acc;
    }, {})
  ).sort((a, b) => b.confidence - a.confidence);

  const totalSessions = profile?.memory?.total_sessions ?? 0;
  const weakAreas = userProfile?.weak_areas ?? [];
  const totalSubmissions = userProfile?.total_submissions ?? 0;

  return (
    <div className="panel-section">
      <div className="panel-label">
        <span className="panel-label-dot" style={{ background: "var(--accent2)", boxShadow: "0 0 6px var(--accent2)" }} />
        Insights
      </div>

      {/* User Stats */}
      {(totalSessions > 0 || totalSubmissions > 0) && (
        <div className="user-stats-row">
          <div className="user-stat">
            <span className="user-stat-value">{totalSessions}</span>
            <span className="user-stat-label">sessions</span>
          </div>
          <div className="user-stat">
            <span className="user-stat-value">{totalSubmissions}</span>
            <span className="user-stat-label">submissions</span>
          </div>
        </div>
      )}

      {/* Weak Areas */}
      {weakAreas.length > 0 && (
        <div className="weak-areas">
          <div className="weak-areas-label">Weak Areas</div>
          <div className="weak-areas-list">
            {weakAreas.map((area, i) => (
              <span key={i} className="weak-area-tag">
                {PATTERN_LABELS[area] || area.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Pattern Bars */}
      {deduped.length === 0 ? (
        <div className="insights-empty">
          Submit code to<br />detect your patterns
        </div>
      ) : (
        deduped.slice(0, 5).map((p, i) => {
          const color = PATTERN_COLORS[p.pattern] || "var(--accent)";
          const confidence = Math.round((p.confidence ?? 0) * 100);
          const label = PATTERN_LABELS[p.pattern] || p.pattern?.replace(/_/g, " ");
          return (
            <div key={i} className="pattern-item">
              <div className="pattern-header">
                <span className="pattern-name">{label}</span>
                <span className="pattern-score" style={{ color }}>{confidence}%</span>
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
        <div className="latest-pattern">
          <span>⚡</span>
          Latest: {PATTERN_LABELS[feedback.pattern_detected] || feedback.pattern_detected.replace(/_/g, " ")}
        </div>
      )}
    </div>
  );
}