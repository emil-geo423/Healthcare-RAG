import { useState } from "react";
import Message from "./Message";
import UploadButton from "./UploadButton";

function ChatWindow({ chats, setChats, activeChat, setActiveChat }) {

  const [input, setInput] = useState("");
  const [showFiles, setShowFiles] = useState(false);

  // -------------------------
  // UPLOAD FILE
  // -------------------------
  const uploadFile = async (file) => {

    let chatIndex = activeChat;

    // Create chat if none
    if (chats.length === 0) {
      const newChat = {
        name: file.name.replace(".pdf", ""),
        messages: [],
        hasFile: true,
        files: []
      };

      setChats([newChat]);
      setActiveChat(0);
      chatIndex = 0;
    }

    // ✅ Instantly show file in UI
    setChats(prev => {
      const copy = [...prev];

      copy[chatIndex] = {
        ...copy[chatIndex],
        hasFile: true,
        files: [
          ...(copy[chatIndex].files || []),
          {
            name: file.name,
            url: URL.createObjectURL(file)
          }
        ]
      };

      return copy;
    });

    // Upload in background
    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch(
        `http://127.0.0.1:8000/upload?session_id=${chatIndex}`,
        { method: "POST", body: form }
      );

      const data = await res.json();

      // Replace temp URL with backend URL
      setChats(prev => {
        const copy = [...prev];

        const index = copy[chatIndex].files.findIndex(
          f => f.name === file.name
        );

        if (index !== -1) {
          copy[chatIndex].files[index].url = data.fileUrl;
        }

        return copy;
      });

    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  // -------------------------
  // SEND MESSAGE
  // -------------------------
  const sendMessage = async () => {

    if (!input.trim()) return;

    const question = input;
    setInput("");

    // Instant UI update
    setChats(prev => {
      const copy = [...prev];

      copy[activeChat].messages.push(
        { role: "user", text: question },
        { role: "bot", text: "Analyzing..." }
      );

      return copy;
    });

    try {

      const res = await fetch(
        `http://127.0.0.1:8000/ask?session_id=${activeChat}&question=${encodeURIComponent(question)}`,
        { method: "POST" }
      );

      const data = await res.json();

      setChats(prev => {
        const copy = [...prev];
        const msgs = [...copy[activeChat].messages];
        msgs[msgs.length - 1] = { role: "bot", text: data.answer };
        copy[activeChat].messages = msgs;
        return copy;
      });

    } catch {

      setChats(prev => {
        const copy = [...prev];
        const msgs = [...copy[activeChat].messages];
        msgs[msgs.length - 1] = { role: "bot", text: "Server error." };
        copy[activeChat].messages = msgs;
        return copy;
      });

    }
  };

  // -------------------------
  // EMPTY CHAT → UPLOAD SCREEN
  // -------------------------
  if (!chats[activeChat]?.hasFile) {
    return (
      <div className="main center-screen">
        <div className="upload-card">

          <div className="upload-icon">📄</div>
          <h2>Upload a document</h2>

          <label className="upload-btn">
            + Choose File
            <input
              type="file"
              hidden
              onChange={(e) => uploadFile(e.target.files[0])}
            />
          </label>

        </div>
      </div>
    );
  }

  // -------------------------
  // NORMAL CHAT VIEW
  // -------------------------
  return (
    <div className="main">

      {/* HEADER */}
      <div className="header">

        <span>Research Assistant</span>

        <div className="header-right">

          <button
            className="files-btn"
            onClick={() => setShowFiles(!showFiles)}
          >
            📁 Files
          </button>

          {showFiles && (
            <div className="files-menu">
              {chats[activeChat].files?.map((f, i) => (
                <a
                  key={i}
                  href={f.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  📄 {f.name}
                </a>
              ))}
            </div>
          )}

        </div>

      </div>

      {/* CHAT AREA */}
      <div className="chat-area">

        {/* Show uploaded files inside chat */}
        {chats[activeChat].files?.map((f, i) => (
          <div key={i} className="file-pill-right">
            📄
            <a href={f.url} target="_blank" rel="noopener noreferrer">
              {f.name}
            </a>
          </div>
        ))}

        <div className="messages">
          {chats[activeChat].messages.map((m, i) => (
            <Message key={i} role={m.role} text={m.text} />
          ))}
        </div>

      </div>

      {/* INPUT BAR */}
      <div className="input-bar">

        <UploadButton uploadFile={uploadFile} />

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button onClick={sendMessage}>Send</button>

      </div>

    </div>
  );
}

export default ChatWindow;




