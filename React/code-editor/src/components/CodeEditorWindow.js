import React, { useState } from "react";
import Editor from "@monaco-editor/react";

// Takes in programming language, theme, code value, and an event trigger for editor changes
const CodeEditorWindow = ({ onChange, language, code, theme }) => {
  const [value, setValue] = useState(code || "");

  const handleEditorChange = (value) => {
    setValue(value);
    onChange("code", value);
  };

  return (
    <div className="overlay rounded-md overflow-hidden w-full h-full shadow-4x1">
      <Editor
        height="85vh"
        width={`100%`}
        language={language || "javascript"}
        value={value}
        theme={theme}
        defaultValue="// Some Comment"
        onChange={handleEditorChange}
      />
    </div>
  );
};

export default CodeEditorWindow;
