# app.py
from flask import Flask, render_template, request, jsonify, session
from sentiment import analyze_sentence_sentiment, analyze_conversation_sentiment
from chatbot import bot_reply
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("CHATBOT_SECRET_KEY", "dev-secret-key-change-me")

# session['conversation'] = [ { 'speaker':'user'/'bot', 'text':..., 'sentiment': {label,emoji,score} } ]

@app.route("/")
def index():
    if "conversation" not in session:
        session["conversation"] = []
    return render_template("index.html")

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.get_json() or {}
    user_text = (data.get("message") or "").strip()
    conv = session.get("conversation", [])

    # analyze user sentence sentiment
    user_sent = analyze_sentence_sentiment(user_text)

    # add user message to conversation
    conv.append({"speaker": "user", "text": user_text, "sentiment": user_sent})

    # generate bot reply (chatbot.py uses internal context memory)
    reply = bot_reply(user_text)
    bot_sent = analyze_sentence_sentiment(reply)

    conv.append({"speaker": "bot", "text": reply, "sentiment": bot_sent})
    session["conversation"] = conv

    return jsonify({
        "reply": reply,
        "user_sentiment": user_sent,
        "conversation": conv
    })

@app.route("/api/end_conversation", methods=["POST"])
def end_conversation():
    conv = session.get("conversation", [])
    user_messages = [c["text"] for c in conv if c["speaker"] == "user"]
    conv_sent = analyze_conversation_sentiment(user_messages)

    # per-message list (user only) with emoji+label
    per_message = []
    for c in conv:
        if c["speaker"] == "user":
            per_message.append({"text": c["text"], "sentiment": c["sentiment"]})

    return jsonify({
        "conversation_sentiment": conv_sent,
        "per_message": per_message,
        "conversation": conv
    })

@app.route("/api/reset", methods=["POST"])
def reset_conv():
    session.pop("conversation", None)
    session["conversation"] = []
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
