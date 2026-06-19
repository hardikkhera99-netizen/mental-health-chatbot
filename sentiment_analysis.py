from transformers import pipeline

# Load sentiment analysis pipeline

sentiment_classifier = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_classifier(text)[0]
    label = result['label']        # 'POSITIVE' or 'NEGATIVE'
    score = round(result['score'], 3)  # Rounded for clarity
    return label, score
