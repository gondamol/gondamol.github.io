"""
Sentiment Analysis for Product Reviews
"""
import logging
from typing import Dict, Tuple
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyze sentiment of product reviews"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_vader(self, text: str) -> Dict:
        """Analyze sentiment using VADER"""
        if not text:
            return None
        
        scores = self.vader.polarity_scores(text)
        
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound'],
        }
    
    def analyze_textblob(self, text: str) -> Dict:
        """Analyze sentiment using TextBlob"""
        if not text:
            return None
        
        blob = TextBlob(text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 to 1
            'subjectivity': blob.sentiment.subjectivity,  # 0 to 1
        }
    
    def get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to label"""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Analyze sentiment and return score and label
        
        Returns:
            Tuple of (score, label)
        """
        if not text:
            return (0.0, 'neutral')
        
        # Use VADER for final score (better for social media/reviews)
        vader_results = self.analyze_vader(text)
        compound = vader_results['compound']
        label = self.get_sentiment_label(compound)
        
        return (compound, label)
    
    def analyze_product_reviews(self, reviews: list) -> Dict:
        """
        Analyze multiple reviews for a product
        
        Args:
            reviews: List of review texts
            
        Returns:
            Dict with aggregated sentiment
        """
        if not reviews:
            return {
                'avg_sentiment': 0.0,
                'sentiment_label': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_reviews': 0,
            }
        
        scores = []
        positive = 0
        negative = 0
        neutral = 0
        
        for review in reviews:
            score, label = self.analyze(review)
            scores.append(score)
            
            if label == 'positive':
                positive += 1
            elif label == 'negative':
                negative += 1
            else:
                neutral += 1
        
        avg_score = sum(scores) / len(scores)
        overall_label = self.get_sentiment_label(avg_score)
        
        return {
            'avg_sentiment': round(avg_score, 3),
            'sentiment_label': overall_label,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'total_reviews': len(reviews),
            'positive_percent': round((positive / len(reviews)) * 100, 1),
            'negative_percent': round((negative / len(reviews)) * 100, 1),
        }






