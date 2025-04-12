"""Chunk Scoring Module.

Scores individual chunks for emotional tone and relatability.
"""

from typing import Dict, Any, List
import json

from loguru import logger
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from ..utils.text_processor import TextProcessor

class ChunkScorer:
    """Scores individual chunks for video selection."""
    
    def __init__(self):
        """Initialize the chunk scorer."""
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Theme categories for tagging
        self.theme_categories = {
            'inspiration': {'inspire', 'motivate', 'encourage', 'possible', 'dream'},
            'insight': {'realize', 'understand', 'learn', 'discover', 'clarity'},
            'expertise': {'know', 'expert', 'experience', 'professional', 'skill'},
            'story': {'happened', 'time', 'when', 'story', 'example'},
            'advice': {'should', 'recommend', 'suggest', 'advice', 'tip'},
            'reflection': {'think', 'feel', 'believe', 'sense', 'perspective'},
            'action': {'do', 'take', 'start', 'begin', 'act'},
            'challenge': {'difficult', 'challenge', 'hard', 'obstacle', 'tough'},
            'success': {'achieve', 'accomplish', 'succeed', 'win', 'goal'},
            'growth': {'grow', 'develop', 'improve', 'progress', 'better'}
        }
    
    def score_chunks(self, transcript: str) -> Dict[str, Any]:
        """Score individual chunks for video selection.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            Dictionary mapping chunk IDs to scores and tags
        """
        logger.info("Starting chunk scoring")
        
        # Extract chunks
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Score each chunk
        scores = {}
        for chunk_id, timestamp, text in chunks:
            scores[chunk_id] = self._score_chunk(text)
        
        logger.info("Completed chunk scoring")
        return scores
    
    def _score_chunk(self, text: str) -> Dict[str, Any]:
        """Score an individual chunk.
        
        Args:
            text: Chunk text content
            
        Returns:
            Dictionary with scores and tags
        """
        # Calculate emotional tone score
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        emotional_score = self._calculate_emotional_score(sentiment)
        
        # Calculate relatability score
        relatability_score = self._calculate_relatability_score(text)
        
        # Generate theme tags
        theme_tags = self._generate_theme_tags(text)
        
        return {
            'emotional_tone_score': round(emotional_score, 2),
            'relatability_score': round(relatability_score, 2),
            'theme_tags': theme_tags
        }
    
    def _calculate_emotional_score(self, sentiment: Dict[str, float]) -> float:
        """Calculate emotional tone score from sentiment.
        
        Args:
            sentiment: VADER sentiment scores
            
        Returns:
            Emotional tone score between 0.00 and 1.00
        """
        # Convert compound score from [-1, 1] to [0, 1]
        base_score = (sentiment['compound'] + 1) / 2
        
        # Adjust for emotional intensity
        intensity = sentiment['pos'] + sentiment['neg']
        
        # Combine base score and intensity
        score = (base_score * 0.7) + (intensity * 0.3)
        
        # Ensure score is in [0, 1]
        return max(0.0, min(1.0, score))
    
    def _calculate_relatability_score(self, text: str) -> float:
        """Calculate relatability score for chunk.
        
        Args:
            text: Chunk text content
            
        Returns:
            Relatability score between 0.00 and 1.00
        """
        score = 0.0
        text_lower = text.lower()
        words = set(text_lower.split())
        
        # Check for personal pronouns (indicates personal story)
        personal_pronouns = {'i', 'me', 'my', 'mine', 'myself'}
        if any(pronoun in words for pronoun in personal_pronouns):
            score += 0.2
        
        # Check for universal experiences
        universal_indicators = {'everyone', 'all', 'we', 'you'}
        if any(indicator in words for indicator in universal_indicators):
            score += 0.2
        
        # Check for emotional words
        emotional_words = {'feel', 'felt', 'emotion', 'experience'}
        if any(word in words for word in emotional_words):
            score += 0.2
        
        # Check for story indicators
        story_indicators = {'when', 'happened', 'time', 'example'}
        if any(indicator in words for indicator in story_indicators):
            score += 0.2
        
        # Check for resolution/insight
        resolution_indicators = {'learned', 'realized', 'understood', 'discovered'}
        if any(indicator in words for indicator in resolution_indicators):
            score += 0.2
        
        # Ensure score is in [0, 1]
        return max(0.0, min(1.0, score))
    
    def _generate_theme_tags(self, text: str) -> List[str]:
        """Generate theme tags for chunk.
        
        Args:
            text: Chunk text content
            
        Returns:
            List of theme tags
        """
        tags = []
        words = set(text.lower().split())
        
        # Check each theme category
        for theme, indicators in self.theme_categories.items():
            if any(indicator in words for indicator in indicators):
                tags.append(theme)
        
        return tags
