import { useState } from "react";

function Sidebar({ chats, setChats, activeChat, setActiveChat, createChat, deleteChat }) {

  const [editingIndex, setEditingIndex] = useState(null);
  const [tempName, setTempName] = useState("");

  const startEditing = (index, currentName) => {
    setEditingIndex(index);
    setTempName(currentName);
  };

  const saveName = (index) => {
  if (!tempName.trim()) return;

  setChats(prev => {
    const copy = [...prev];
    copy[index] = {
      ...copy[index],
      name: tempName
    };
    return copy;
  });

  setEditingIndex(null);
};


  return (
    <div className="sidebar">

  <h2>Chats</h2>

  {/* Search */}
  <input
    className="chat-search"
    placeholder="Search chats..."
  />

  {/* New Chat */}
  <button onClick={createChat} className="new-chat-btn">
    + New Chat
  </button>

  {/* Chat List */}
  <div className="chat-list">
    <h2>Chat List</h2>
    <p>___________________________</p><br></br>

    {chats.map((chat, i) => (

      <div
        key={i}
        className={`chat-item ${i === activeChat ? "active" : ""}`}
        onClick={() => setActiveChat(i)}
      >

        {/* Chat Name */}
        {editingIndex === i ? (
          <input
            className="rename-input"
            value={tempName}
            autoFocus
            onChange={(e) => setTempName(e.target.value)}
            onBlur={() => saveName(i)}
            onKeyDown={(e) => e.key === "Enter" && saveName(i)}
          />
        ) : (
          <span className="chat-name">{chat.name}</span>
        )}

        {/* Three Dot Menu */}
        <div
          className="chat-menu"
          onClick={(e) => e.stopPropagation()}
        >
          ⋮

          <div className="chat-menu-dropdown">

            <div
              onClick={() => startEditing(i, chat.name)}
            >
               Rename
            </div>

            <div
              className="danger"
              onClick={() => deleteChat(i)}
            >
               Delete
            </div>

          </div>

        </div>

      </div>

    ))}

  </div>

</div>

  );
}

export default Sidebar;

