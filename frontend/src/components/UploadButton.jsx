import { useRef } from "react";

function UploadButton({ uploadFile }) {

  const fileRef = useRef();

  return (
    <>
      <button
        className="plus-btn"
        onClick={() => fileRef.current.click()}
      >
        +
      </button>

      <input
        type="file"
        hidden
        ref={fileRef}
        onChange={(e) => uploadFile(e.target.files[0])}
      />
    </>
  );
}

export default UploadButton;
