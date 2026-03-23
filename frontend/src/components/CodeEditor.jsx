import Editor from "@monaco-editor/react";

export default function CodeEditor({ code, onChange }) {
  return (
    <div className="editor-wrapper">
      <Editor
        height="100%"
        defaultLanguage="python"
        value={code}
        onChange={(val) => onChange(val || "")}
        theme="vs-dark"
        options={{
          fontSize: 14,
          fontFamily: "'JetBrains Mono', monospace",
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          lineNumbers: "on",
          renderLineHighlight: "line",
          tabSize: 4,
          insertSpaces: true,
          wordWrap: "on",
          padding: { top: 16, bottom: 16 },
          smoothScrolling: true,
        }}
      />
    </div>
  );
}
