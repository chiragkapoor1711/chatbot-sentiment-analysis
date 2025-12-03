# Chatbot With Sentiment Analysis  
A Python + Flask based chatbot that interacts with the user, maintains conversation history, and performs sentiment analysis at both conversation level  and message level.

---

## 🚀 Features
### ✅ Tier 1 – Mandatory
- Maintains full conversation history  
- Performs **overall sentiment analysis** at the end of the chat  
- Shows whether the overall mood was **Positive**, **Negative**, or **Neutral**

### ⭐ Tier 2 – Additional Credit
- Performs **sentiment analysis on every user message**
- Displays the sentiment label in real-time (Positive / Negative / Neutral)
- Shows a **trend/shift in mood** based on message sequence  
  (e.g., *Mood is improving*, *Mood is becoming negative*)

### 🔥 Enhancements / Innovation
- Realistic chatbot replies (context-aware rule-based system)
- Expanded emotional vocabulary (happy/sad expressions)
- Emoji-based sentiment indicators
- Clean UI similar to modern chat apps
- Session-based conversation memory
- Modular code design (easy to extend or replace components)

---

## 🧠 Technologies Used
- **Python 3**
- **Flask (Backend Web Framework)**
- **TextBlob** (Sentiment Analysis)
- **HTML, CSS, JavaScript** (Frontend)
- **Session Storage** for conversation memory

---
## 📂 Project Structure
chatbot-sentiment/
│── app.py # Flask server
│── sentiment.py # Sentiment logic (TextBlob)
│── chatbot.py # Chatbot reply logic
│── static/
│ ├── style.css # UI styling
│ └── app.js # Frontend logic
│── templates/
│ └── index.html # UI page
│── tests/
│ └── test_sentiment.py # Unit tests (optional)
│── README.md
│── requirements.txt

### 1️⃣ Create & activate virtual environment
python -m venv venv

### 2️⃣ Install dependencies

### 3️⃣ Run the Flask app

### 4️⃣ Open in browser

Chat with the bot → Click **End Chat** → See final sentiment result.

---

## 🧠 How Sentiment Logic Works

### ✔ Sentence-Level Sentiment (Tier 2)
Every user message is analyzed with **TextBlob polarity**:

- **polarity > 0** → Positive  
- **polarity < 0** → Negative  
- **polarity = 0** → Neutral  

This sentiment is shown next to each message in the UI.

---

### ✔ Conversation-Level Sentiment (Tier 1)
At the end:

1. All user messages are collected  
2. Their polarity scores are averaged  
3. The **overall mood** is determined:

| Score Range                 | Sentiment |
|----------------------------|-----------|
| > 0                        | Positive  |
| < 0                        | Negative  |
| = 0                        | Neutral   |

---

### ⭐ Mood Trend (Bonus)
Based on message polarity over time:
- If later messages are more positive → **Mood improving**
- If later messages are more negative → **Mood declining**
- Otherwise → **Mood stable**

This is optional but included for extra credit.

---

## 🧪 Tests (if implemented)

Run:

Tests include:
- Positive sentiment detection  
- Negative sentiment detection  
- Neutral sentiment handling  
- Overall conversation sentiment calculation  

---

## ✨ Possible Enhancements
- Integrate an AI-based chatbot (HuggingFace models)
- Add speech-to-text and text-to-speech
- Add conversation export to PDF
- Add sentiment graph visualization
- Save chat history in database

---

## 📌 Status
- **Tier 1: FULLY IMPLEMENTED ✅**  
- **Tier 2: FULLY IMPLEMENTED (+ mood trend) ⭐**  

---

## 👨‍💻 Author
Developed by **Chirag Kapoor**  



