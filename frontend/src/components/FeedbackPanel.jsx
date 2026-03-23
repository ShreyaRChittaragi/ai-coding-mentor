export default function FeedbackPanel({ feedback, error, loading, mode }) {
  if (loading) {
    return (
      <div className="panel-section" style={{ flex: 1 }}>
        <div className="panel-label">
          <span className="panel-label-dot" />
          {mode === "hint" ? "Getting hint..." : "Feedback"}
        </div>
        <div className="feedback-loading">
          <span className="spinner" style={{
            width: 16, height: 16,
            borderColor: "rgba(0,217,163,0.2)",
            borderTopColor: "var(--accent)"
          }} />
          {mode === "hint" ? "Thinking..." : "Evaluating your code..."}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel-section" style={{ flex: 1 }}>
        <div className="panel-label">
          <span className="panel-label-dot" style={{ background: "var(--error)", boxShadow: "0 0 6px var(--error)" }} />
          Feedback
        </div>
        <div className="feedback-error">⚠ {error}</div>
      </div>
    );
  }

  if (!feedback) {
    return (
      <div className="panel-section" style={{ flex: 1 }}>
        <div className="panel-label">
          <span className="panel-label-dot" style={{ background: "var(--text-dim)", boxShadow: "none" }} />
          Feedback
        </div>
        <div className="feedback-empty">
          <span className="feedback-empty-icon">⌥</span>
          Submit your code<br />to get personalized feedback
        </div>
      </div>
    );
  }

  const passed = feedback.eval_result?.all_passed;
  const passedCount = feedback.eval_result?.passed_count ?? "–";
  const total = feedback.eval_result?.total ?? "–";
  const execTime = feedback.eval_result?.execution_time_ms;
  const edgeCases = feedback.eval_result?.edge_case_results ?? [];
  const errorTypes = feedback.eval_result?.error_types ?? [];

  return (
    <div className="panel-section" style={{ flex: 1, overflowY: "auto" }}>
      <div className="panel-label">
        <span className="panel-label-dot" style={{
          background: mode === "hint" ? "var(--accent2)" : passed ? "var(--success)" : "var(--error)",
          boxShadow: mode === "hint" ? "0 0 6px var(--accent2)" : passed ? "0 0 6px var(--success)" : "0 0 6px var(--error)"
        }} />
        {mode === "hint" ? "💡 Hint" : "Feedback"}
      </div>

      {mode !== "hint" && (
        <>
          <div className={`result-banner ${passed ? "result-pass" : "result-fail"}`}>
            <span className="result-icon">{passed ? "✓" : "✗"}</span>
            {passed ? "All Tests Passed" : "Tests Failed"}
          </div>

          <div className="test-stats">
            <span className="stat-chip">
              {passed ? "✓" : "✗"} {passedCount}/{total} passed
            </span>
            {execTime !== undefined && (
              <span className="stat-chip">⏱ {execTime}ms</span>
            )}
            {errorTypes.map((e, i) => (
              <span key={i} className="stat-chip stat-chip-error">{e}</span>
            ))}
          </div>
        </>
      )}

      {feedback.feedback && (
        <div className="hint-box">
          <div className="hint-label">✦ Mentor Hint</div>
          <div className="hint-text">{feedback.feedback}</div>
        </div>
      )}

      {edgeCases.length > 0 && mode !== "hint" && (
        <>
          <div className="section-label">Test Cases</div>
          {edgeCases.map((tc) => (
            <div
              key={tc.case_index}
              className={`test-case ${tc.passed ? "test-case-pass" : "test-case-fail"}`}
            >
              <div className="test-case-header">
                <span className="test-case-index">Case #{tc.case_index + 1}</span>
                <span className={tc.passed ? "test-status-pass" : "test-status-fail"}>
                  {tc.passed ? "PASS" : "FAIL"}
                </span>
              </div>
              {!tc.passed && (
                <>
                  <div className="test-detail">
                    <span style={{ color: "var(--text-dim)" }}>Expected: </span>
                    {JSON.stringify(tc.expected)}
                  </div>
                  <div className="test-detail">
                    <span style={{ color: "var(--text-dim)" }}>Got: </span>
                    {JSON.stringify(tc.actual)}
                  </div>
                  {tc.error && (
                    <div className="test-detail" style={{ color: "var(--error)" }}>
                      {tc.error}
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  );
}