async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

      // Show user message
    const userMsg = document.createElement("div");
    userMsg.className = "user-message";
    userMsg.textContent = message;
    chatBox.appendChild(userMsg);

    // Show "Thinking..." loader
    const botMsg = document.createElement("div");
    botMsg.className = "bot-message";
    botMsg.textContent = "🤔 Thinking...";
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    try {
        const res = await fetch("/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        });

        const data = await res.json();
        botMsg.innerHTML = marked.parse(data.reply);
      } catch (err) {
        botMsg.textContent = "❌ Failed to fetch response.";
      }
        chatBox.scrollTop = chatBox.scrollHeight;
    }