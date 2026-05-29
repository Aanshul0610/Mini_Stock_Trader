import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download("vader_lexicon")

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound > 0.05:
        label = "Positive"
    elif compound < -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "score": compound
    }