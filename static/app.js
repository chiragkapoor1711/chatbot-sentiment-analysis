// static/app.js (final — shows only sentiment label, no emoji)
const input = document.getElementById("inputMessage");
const sendBtn = document.getElementById("sendBtn");
const messagesDiv = document.getElementById("messages");
const messageListDiv = document.getElementById("messageList");
const endBtn = document.getElementById("endBtn");
const resetBtn = document.getElementById("resetBtn");
const finalSummary = document.getElementById("finalSummary");
const overallLabel = document.getElementById("overallLabel");
const overallScore = document.getElementById("overallScore");

function createBubble(text, cls) {
  const wrap = document.createElement("div");
  wrap.style.display = "flex";
  wrap.style.flexDirection = "column";
  wrap.style.alignItems = cls === "user" ? "flex-end" : "flex-start";

  const b = document.createElement("div");
  b.className = `bubble ${cls}`;
  b.innerText = text;

  wrap.appendChild(b);
  return wrap;
}

function addMessageToList(text, sentiment) {
  // remove placeholder if first message
  if (messageListDiv.querySelector('em')) {
    messageListDiv.innerHTML = '';
  }

  const item = document.createElement("div");
  item.style.display = "flex";
  item.style.justifyContent = "space-between";
  item.style.alignItems = "center";
  item.style.padding = "6px 8px";
  item.style.borderLeft = "4px solid transparent";
  item.style.borderRadius = "6px";
  item.style.gap = "8px";

  // truncated text preview
  const preview = document.createElement("div");
  preview.style.flex = "1";
  preview.style.marginRight = "8px";
  preview.style.fontSize = "14px";
  preview.style.color = "var(--text-muted, #475569)";
  preview.innerText = text.length > 60 ? text.substring(0, 60) + "..." : text;

  // badge showing only label (no emoji)
  const badge = document.createElement("span");
  badge.className = "badge " + (sentiment.label === "Positive" ? "pos" : (sentiment.label === "Negative" ? "neg" : "neu"));
  badge.innerText = sentiment.label; // <-- only label here

  // optional: left border color to indicate sentiment
  const borderColor = sentiment.label === "Positive" ? "var(--green, #10b981)" :
                      sentiment.label === "Negative" ? "var(--red, #ef4444)" : "var(--muted, #6b7280)";
  item.style.borderLeftColor = borderColor;

  item.appendChild(preview);
  item.appendChild(badge);
  messageListDiv.prepend(item);
}

async function sendMessage() {
  const txt = input.value.trim();
  if (!txt) return;

  // local show user message
  messagesDiv.appendChild(createBubble(txt, "user"));
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  input.value = "";
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: txt })
    });

    // handle non-JSON response gracefully
    const contentType = res.headers.get("content-type") || "";
    if (!res.ok) {
      // show error message from server (if HTML, display friendly text)
      const text = await res.text();
      console.error("Server error response:", text);
      messagesDiv.appendChild(createBubble("Sorry, server returned an error.", "bot"));
      return;
    }
    if (!contentType.includes("application/json")) {
      const text = await res.text();
      console.error("Expected JSON but got:", text);
      messagesDiv.appendChild(createBubble("Unexpected server response.", "bot"));
      return;
    }

    const data = await res.json();

    // show bot reply
    messagesDiv.appendChild(createBubble(data.reply, "bot"));
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Update statement-level list with label only
    // data.user_sentiment should be like { label: "Positive", score: 0.7 }
    if (data.user_sentiment && data.user_sentiment.label) {
      addMessageToList(txt, data.user_sentiment);
    } else {
      // fallback if sentiment missing
      addMessageToList(txt, { label: "Neutral" });
    }

  } catch (error) {
    console.error("Error sending message:", error);
    messagesDiv.appendChild(createBubble("Sorry, there was an error processing your message.", "bot"));
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

endBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/api/end_conversation", { method: "POST" });
    if (!res.ok) {
      const t = await res.text();
      console.error("End conversation error:", t);
      return;
    }
    const data = await res.json();
    const convSent = data.conversation_sentiment;

    finalSummary.style.display = "block";
    // show only label (no emoji)
    overallLabel.className = "overall-label " +
      (convSent.label === "Positive" ? "positive" :
       convSent.label === "Negative" ? "negative" : "neutral");

    overallLabel.innerText = convSent.label; // <-- only label
    overallScore.innerText = `Average score: ${convSent.score_avg !== undefined ? convSent.score_avg.toFixed(3) : "0.000"}`;

  } catch (error) {
    console.error("Error ending conversation:", error);
  }
});

resetBtn.addEventListener("click", async () => {
  try {
    await fetch("/api/reset", { method: "POST" });
    messagesDiv.innerHTML = "";
    messageListDiv.innerHTML = "<em style='color: var(--text-muted);'>No messages yet. Start chatting!</em>";
    finalSummary.style.display = "none";
  } catch (error) {
    console.error("Error resetting:", error);
  }
});

input.focus();
