# sentiment.py
"""
Lightweight sentiment analysis using small built-in lexicons.
Returns:
 - analyze_sentence_sentiment(text) -> { label: "Positive"/"Negative"/"Neutral", emoji: "😃"/"😞"/"😐", score: float, display: "😃 Positive" }
 - analyze_conversation_sentiment(list_of_user_messages) -> { label, emoji, score_avg, trend, display }
"""

from typing import List

# small positive and negative word lists (extend if you want)
POS_WORDS = {
    "good", "great", "awesome", "amazing", "happy", "love", "liked", "nice", "better",
    "fantastic", "satisfied", "excellent", "cool", "wonderful", "enjoyed"
}
NEG_WORDS = {
    "bad", "worst", "awful", "hate", "disappointed", "sad", "angry", "upset", "terrible",
    "poor", "frustrated", "problem", "issue", "annoyed", "hurt", "dissatisfied"
}


def _score_text(text: str) -> float:
    """
    Very simple scoring:
    score = (count_positive - count_negative) / total_words
    Range roughly -1 .. +1 (depends on text)
    """
    if not text or not text.strip():
        return 0.0
    words = [w.strip(".,!?;:\"'()[]").lower() for w in text.split()]
    if not words:
        return 0.0

    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    total = len(words)
    return (pos - neg) / total


def _label_for_score(score: float) -> str:
    # thresholds: small positive/negative margin to avoid neutral on tiny values
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def _emoji_for_label(label: str) -> str:
    return {
        "Positive": "😃",
        "Negative": "😞",
        "Neutral": "😐"
    }.get(label, "😐")


def analyze_sentence_sentiment(text: str):
    """
    Returns { 'label': ..., 'emoji': '😃', 'score': float, 'display': '😃 Positive' }
    The 'display' field combines emoji and label for easy UI rendering.
    """
    s = _score_text(text)
    label = _label_for_score(s)
    emoji = _emoji_for_label(label)
    display = f"{emoji} {label}"
    return {"label": label, "emoji": emoji, "score": s, "display": display}


def analyze_conversation_sentiment(user_messages: List[str]):
    """
    Compute average score across user messages and return label + emoji + trend + display.
    Trend: simple comparison between first half avg and second half avg:
      - "Improving" if second_avg > first_avg by threshold
      - "Getting worse" if second_avg < first_avg by threshold
      - "Stable" otherwise
    """
    msgs = [m for m in user_messages if m and m.strip()]
    if not msgs:
        neutral_emoji = _emoji_for_label("Neutral")
        return {
            "label": "Neutral",
            "emoji": neutral_emoji,
            "score_avg": 0.0,
            "trend": "No messages",
            "display": f"{neutral_emoji} Neutral"
        }

    scores = [_score_text(m) for m in msgs]
    avg = sum(scores) / len(scores)
    label = _label_for_score(avg)
    emoji = _emoji_for_label(label)
    display = f"{emoji} {label}"

    # trend detection
    if len(scores) >= 2:
        mid = len(scores) // 2
        first_avg = sum(scores[:mid]) / max(1, len(scores[:mid]))
        second_avg = sum(scores[mid:]) / max(1, len(scores[mid:]))
        diff = second_avg - first_avg
        # threshold for meaningful change
        if diff >= 0.03:
            trend = "Mood improving"
        elif diff <= -0.03:
            trend = "Mood getting worse"
        else:
            trend = "Mood stable"
    else:
        trend = "Not enough data for trend"

    return {
        "label": label,
        "emoji": emoji,
        "score_avg": avg,
        "trend": trend,
        "per_message_scores": scores,
        "display": display
    }


# Example usage:
if __name__ == "__main__":
    # Test single sentence
    result1 = analyze_sentence_sentiment("I love this amazing product!")
    print(f"Sentence: {result1['display']}")  # Output: 😃 Positive

    # Test conversation
    messages = [
        "This is terrible and I'm upset",
        "Things are getting better now",
        "I'm really happy with the service!"
    ]
    result2 = analyze_conversation_sentiment(messages)
    print(f"Conversation: {result2['display']}")  # Output: 😃/😞/😐 + Label
    print(f"Trend: {result2['trend']}")