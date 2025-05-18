from enum import Enum


class Mood(str, Enum):
    happy = "happy"
    sad = "sad"
    neutral = "neutral"
