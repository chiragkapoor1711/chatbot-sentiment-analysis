import random

CONTEXT_MEMORY = {"last_user_message": ""}

# ---------------------------------------------
# LARGE REALISTIC WORD LISTS
# ---------------------------------------------

GREETINGS = [
    "hello", "hi", "hey", "namaste", "hola", "yo", "sup", "good morning",
    "good evening", "good afternoon", "greetings"
]

THANKS = [
    "thanks", "thank you", "thnx", "ty", "thanku", "thanks a lot",
    "really appreciate", "appreciate it"
]

SAD_WORDS = [
    "sad", "unhappy", "depressed", "disappointed", "frustrated", "angry",
    "upset", "bad", "hurt", "pain", "annoyed", "tired", "stressed",
    "worried", "anxious", "scared", "fear", "broken", "terrible",
    "horrible", "cry", "crying", "pathetic", "hate", "angry", "rage",
    "irritated", "lonely", "hopeless", "miserable"
]

GOOD_WORDS = [
    "good", "great", "fine", "better", "happy", "amazing", "nice",
    "awesome", "cool", "fantastic", "wonderful", "excellent", "joy",
    "excited", "love", "enjoy", "perfect", "beautiful", "awesome",
    "brilliant", "delight", "positive", "grateful"
]

CONFUSION_WORDS = [
    "confused", "don't know", "not sure", "unsure", "what should i do",
    "lost", "no idea", "idk"
]

ANGER_WORDS = [
    "angry", "mad", "furious", "rage", "irritated", "annoyed", "pissed"
]

STRESS_WORDS = [
    "stress", "stressed", "anxiety", "anxious", "pressure", "overthinking",
    "panic", "panic attack", "tensed", "tense"
]

APPRECIATION_WORDS = [
    "good job", "nice work", "amazing work", "i appreciate", "proud of",
    "helpful", "you're great"
]

# ---------------------------------------------
# NATURAL HUMAN-LIKE RESPONSES
# ---------------------------------------------

GENERIC_REPLIES = [
    "I get you… wanna explain a bit more?",
    "Hmm okay… what happened exactly?",
    "I understand… continue.",
    "Alright… I'm listening carefully.",
    "Okay… tell me more about it.",
    "Hmm… interesting. Go on.",
    "I see… how do you feel about that?",
    "I hear you… what happened next?",
]

FOLLOW_UP_QUESTIONS = [
    "And how did that make you feel?",
    "Why do you think that happened?",
    "What do you want to improve?",
    "What do you think would help next?",
    "What do you expect to happen now?",
    "Do you want things to change?",
]

POSITIVE_REPLIES = [
    "Wow, that sounds amazing! 😊",
    "That's great! What made it so good?",
    "Happy to hear that! Tell me more!",
    "Nice! I'm glad things are going well. 😄",
    "Awesome! What else happened?",
]

NEGATIVE_REPLIES = [
    "I'm really sorry you're going through this 😞",
    "That must be really difficult… I'm here with you.",
    "I understand… that sounds painful.",
    "You don’t deserve to feel this way…",
    "It’s okay to feel like this sometimes.",
]

CONFUSION_REPLIES = [
    "It’s okay to feel confused… let’s figure this out together.",
    "Hmm… what part confuses you the most?",
    "Alright, let’s clarify it step by step.",
]

ANGER_REPLIES = [
    "I can sense the frustration… what triggered it?",
    "That sounds really upsetting… want to share more?",
    "It's okay to vent… I'm listening.",
]

STRESS_REPLIES = [
    "Stress can be really heavy… want to talk about it?",
    "That sounds overwhelming… what’s causing the pressure?",
    "I get it… anxiety can be tough. You’re not alone.",
]

APPRECIATION_REPLIES = [
    "Thank you! That means a lot 😊",
    "Glad I could help! Want to talk more?",
    "Happy to assist anytime!",
]

# ---------------------------------------------
# FINAL ADVANCED BOT REPLY LOGIC
# ---------------------------------------------

def bot_reply(user_message: str):
    txt = (user_message or "").lower()
    CONTEXT_MEMORY["last_user_message"] = user_message

    # greetings
    if any(w == txt or w in txt.split() for w in GREETINGS):
        return random.choice([
            "Hello! How are you feeling today?",
            "Hi! I'm here to chat. What's up?",
            "Hey! What's going on in your mind?"
        ])

    # thanks
    if any(w in txt for w in THANKS):
        return random.choice(APPRECIATION_REPLIES)

    # confusion
    if any(w in txt for w in CONFUSION_WORDS):
        return random.choice(CONFUSION_REPLIES)

    # anger
    if any(w in txt for w in ANGER_WORDS):
        return random.choice(ANGER_REPLIES) + " " + random.choice(FOLLOW_UP_QUESTIONS)

    # stress / anxiety
    if any(w in txt for w in STRESS_WORDS):
        return random.choice(STRESS_REPLIES)

    # sad / negative
    if any(w in txt for w in SAD_WORDS):
        return random.choice(NEGATIVE_REPLIES) + " " + random.choice(FOLLOW_UP_QUESTIONS)

    # good / positive
    if any(w in txt for w in GOOD_WORDS):
        return random.choice(POSITIVE_REPLIES)

    # meaningful word: why
    if "why" in txt:
        return "That's a good question… what do YOU think the reason might be?"

    # meaningful word: because
    if "because" in txt:
        return "Hmm… that makes sense. Continue…"

    # fallback
    return random.choice(GENERIC_REPLIES)
