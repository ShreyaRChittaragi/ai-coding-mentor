import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Legend, CartesianGrid
} from "recharts";

const PATTERN_COLORS = {
  overthinking:      "#7c6ff7",
  guessing:          "#f59e0b",
  concept_gap:       "#f87171",
  boundary_weakness: "#38bdf8",
  rushing:           "#fb923c",
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: "#1a1e2a",
        border: "1px solid #252a38",
        borderRadius: "6px",
        padding: "8px 12px",
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: "11px",
      }}>
        <div style={{ color: "#64748b", marginBottom: "4px" }}>Session {label}</div>
        {payload.map((p, i) => (
          <div key={i} style={{ color: p.color }}>
            {p.name}: {Math.round(p.value * 100)}%
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export default function PatternChart({ userId, apiBase }) {
  const [chartData, setChartData] = useState([]);
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchViz = async () => {
      try {
        const res = await fetch(`${apiBase}/visualizations/${userId}`);
        if (!res.ok) return;
        const data = await res.json();

        const trends = data.pattern_trends ?? [];

        // Group by session number
        const sessionMap = {};
        trends.forEach(t => {
          const key = t.session ?? t.detected_at;
          if (!sessionMap[key]) sessionMap[key] = { session: key };
          sessionMap[key][t.pattern] = t.confidence;
        });

        const chartRows = Object.values(sessionMap);
        const uniquePatterns = [...new Set(trends.map(t => t.pattern))];

        setChartData(chartRows);
        setPatterns(uniquePatterns);
      } catch (_) {}
      finally { setLoading(false); }
    };

    fetchViz();
  }, [userId]);

  if (loading) return null;
  if (chartData.length === 0) return null;

  return (
    <div className="panel-card">
      <div className="panel-title">Pattern Trends</div>
      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={chartData} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#252a38" />
          <XAxis
            dataKey="session"
            tick={{ fontFamily: "'JetBrains Mono'", fontSize: 10, fill: "#64748b" }}
            label={{ value: "Session", position: "insideBottom", offset: -2, fontSize: 10, fill: "#64748b" }}
          />
          <YAxis
            domain={[0, 1]}
            tickFormatter={v => `${Math.round(v * 100)}%`}
            tick={{ fontFamily: "'JetBrains Mono'", fontSize: 10, fill: "#64748b" }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontFamily: "'JetBrains Mono'", fontSize: 10, paddingTop: "8px" }}
          />
          {patterns.map(p => (
            <Line
              key={p}
              type="monotone"
              dataKey={p}
              stroke={PATTERN_COLORS[p] || "#00e5a0"}
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
