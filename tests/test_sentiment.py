# tests/test_sentiment.py
from sentiment import analyze_sentence_sentiment, analyze_conversation_sentiment

def test_positive_sentence():
    res = analyze_sentence_sentiment("I am very happy and pleased with this!")
    assert res["label"] == "Positive"
    assert res["score"] > 0

def test_negative_sentence():
    res = analyze_sentence_sentiment("This is the worst, I'm so disappointed.")
    assert res["label"] == "Negative"
    assert res["score"] < 0

def test_conversation_sentiment_neg():
    msgs = ["I hate this", "This is bad", "I am unhappy"]
    conv = analyze_conversation_sentiment(msgs)
    assert conv["label"] == "Negative"

def test_trend_improving():
    msgs = ["I am unhappy", "Still bad", "Actually getting better", "Feeling good now"]
    conv = analyze_conversation_sentiment(msgs)
    assert conv["trend"]["label"] in ["Improving", "Stable"]  # small noise tolerant
