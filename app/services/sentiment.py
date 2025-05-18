from textblob import TextBlob
from app.schemas.mood import Mood


def analyze_sentiment(text: str) -> Mood:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return Mood.happy
    elif polarity < -0.3:
        return Mood.sad
    else:
        return Mood.neutral
