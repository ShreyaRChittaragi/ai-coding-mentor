export default function FeedbackPanel({ feedback, error, loading }) {
    if (loading) {
      return (
        <div className="panel-card" style={{ flex: 1 }}>
          <div className="panel-title">Feedback</div>
          <div className="feedback-loading">
            <span className="spinner" style={{ borderColor: "#00e5a0", borderTopColor: "transparent" }} />
            Evaluating your code...
          </div>
        </div>
      );
    }
  
    if (error) {
      return (
        <div className="panel-card" style={{ flex: 1 }}>
          <div className="panel-title">Feedback</div>
          <div className="feedback-error">⚠ {error}</div>
        </div>
      );
    }
  
    if (!feedback) {
      return (
        <div className="panel-card" style={{ flex: 1 }}>
          <div className="panel-title">Feedback</div>
          <div className="feedback-empty">
            Submit your code<br />to get feedback
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
      <div className="panel-card" style={{ flex: 1, overflowY: "auto" }}>
        <div className="panel-title">Feedback</div>
  
        <div className={`result-badge ${passed ? "result-pass" : "result-fail"}`}>
          {passed ? "✓ All Tests Passed" : "✗ Tests Failed"}
        </div>
  
        <div className="test-stats">
          <span className="stat-chip">✓ {passedCount}/{total} passed</span>
          {execTime !== undefined && (
            <span className="stat-chip">⏱ {execTime}ms</span>
          )}
          {errorTypes.map((e, i) => (
            <span key={i} className="stat-chip" style={{ color: "var(--error)" }}>{e}</span>
          ))}
        </div>
  
        {feedback.feedback && (
          <>
            <div className="section-label">Mentor Hint</div>
            <div className="feedback-text">{feedback.feedback}</div>
          </>
        )}
  
        {edgeCases.length > 0 && (
          <>
            <div className="section-label">Test Cases</div>
            {edgeCases.map((tc) => (
              <div key={tc.case_index} className={`test-case ${tc.passed ? "test-case-pass" : "test-case-fail"}`}>
                <div className="test-case-header">
                  <span className="test-case-index">Case #{tc.case_index + 1}</span>
                  <span className={tc.passed ? "test-status-pass" : "test-status-fail"}>
                    {tc.passed ? "PASS" : "FAIL"}
                  </span>
                </div>
                {!tc.passed && (
                  <>
                    <div className="test-detail">Expected: {JSON.stringify(tc.expected)}</div>
                    <div className="test-detail">Got: {JSON.stringify(tc.actual)}</div>
                    {tc.error && <div className="test-detail" style={{ color: "var(--error)" }}>{tc.error}</div>}
                  </>
                )}
                {tc.passed && (
                  <div className="test-detail" style={{ color: "#4ade80", opacity: 0.7 }}>
                    Input: {JSON.stringify(tc.input)}
                  </div>
                )}
              </div>
            ))}
          </>
        )}
      </div>
    );
  }
  