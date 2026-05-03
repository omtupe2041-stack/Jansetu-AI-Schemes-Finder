document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  let isSending = false;

  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}-message`;
    msg.innerHTML = text.replace(/\n/g, "<br>");
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showTyping() {
    const t = document.createElement("div");
    t.className = "message bot-message typing";
    t.id = "typingIndicator";
    t.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
    chatBox.appendChild(t);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById("typingIndicator");
    if (t) t.remove();
  }

  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || isSending) return;

    appendMessage(text, "user");
    userInput.value = "";
    showTyping();
    isSending = true;

    try {
      const res = await fetch("/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      const data = await res.json();
      removeTyping();
      appendMessage(data.reply || "⚠ No response received.", "bot");
    } catch (err) {
      removeTyping();
      appendMessage("⚠ त्रुटी आली. पुन्हा प्रयत्न करा.", "bot");
      console.error(err);
    }

    isSending = false;
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Quick prompt helper
  window.prefill = (txt) => {
    userInput.value = txt;
    userInput.focus();
  };
});
