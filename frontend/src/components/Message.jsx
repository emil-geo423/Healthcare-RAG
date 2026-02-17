function Message({ role, text }) {
  return (
    <div className={role === "user" ? "user-msg" : "bot-msg"}>
      {text}
    </div>
  );
}

export default Message;
