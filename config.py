DEPARTMENTS = ["Arts", "Business", "Engineering", "Medical", "Science"]

RISK_THRESHOLDS = {
    "low": 30,
    "moderate": 60
}

QUESTIONS = {
    "age": "What's your age?",
    "gender": "What's your gender? (Male/Female)",
    "cgpa": "What's your CGPA? (0.0 - 4.0)",
    "sleep": "How many hours do you typically sleep per night?",
    "study": "How many hours do you study per day?",
    "social_media": "How many hours do you spend on social media daily?",
    "exercise": "How many minutes of exercise do you get per week?",
    "stress": "On a scale of 0-10, how stressed are you? (0 = no stress, 10 = extreme)",
    "department": f"What's your department? ({', '.join(DEPARTMENTS)})"
}

CRISIS_RESOURCES = """
- Suicide Prevention: 988
- Crisis Text: Text HOME to 741741
- International: iasp.info
"""