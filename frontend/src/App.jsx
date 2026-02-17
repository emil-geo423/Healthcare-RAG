import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./index.css";

function App() {

  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(0);

  // ---------------------
  //NEW CHAT
  // ---------------------
  const newChat = {
  name: `Chat ${chats.length + 1}`,
  messages: [],
  hasFile: false,
  files: []   // ✅
};


  // ---------------------
  // CREATE NEW CHAT
  // ---------------------
  const createChat = () => {
    const newChat = {
      name: `Chat ${chats.length + 1}`,
      messages: [],
      hasFile: false,
      fileName: "",
      fileUrl: ""
    };

    setChats(prev => [...prev, newChat]);
    setActiveChat(chats.length);
  };

  // ---------------------
  // DELETE CHAT
  // ---------------------
  const deleteChat = (index) => {
  const updated = chats.filter((_, i) => i !== index);
  setChats(updated);
  setActiveChat(0);
};


  return (
    <div className="app">

      <Sidebar
        chats={chats}
        setChats={setChats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        createChat={createChat}
        deleteChat={deleteChat}
      />

      <ChatWindow
        chats={chats}
        setChats={setChats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        createChat={createChat}
      />

    </div>
  );
}

export default App;






