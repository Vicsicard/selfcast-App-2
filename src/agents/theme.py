"""Theme Extraction Agent.

Identifies central narratives and recurring concepts in the transcript.
"""

from typing import List, Dict, Set
from collections import Counter

from loguru import logger
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from .base import BaseAgent
from ..utils.text_processor import TextProcessor

class ThemeExtractor(BaseAgent):
    """Extracts central themes and narrative arcs."""
    
    def __init__(self):
        """Initialize the theme extractor."""
        self.text_processor = TextProcessor()
        self.stop_words = set(stopwords.words('english'))
        
        # Common theme categories
        self.theme_indicators = {
            'growth': {'learn', 'grow', 'develop', 'improve', 'progress', 'journey'},
            'challenge': {'difficult', 'challenge', 'obstacle', 'struggle', 'overcome'},
            'change': {'change', 'transition', 'shift', 'transform', 'adapt'},
            'purpose': {'purpose', 'meaning', 'mission', 'calling', 'passion'},
            'relationships': {'team', 'people', 'connection', 'community', 'support'},
            'achievement': {'accomplish', 'achieve', 'success', 'goal', 'milestone'},
            'resilience': {'persist', 'endure', 'resilient', 'bounce', 'recover'},
            'authenticity': {'authentic', 'genuine', 'true', 'real', 'honest'}
        }
    
    def analyze(self, transcript: str) -> List[str]:
        """Extract themes from the transcript.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of identified themes as bullet points
        """
        logger.info("Starting theme extraction")
        
        # Clean transcript
        clean_text = self._clean_transcript(transcript)
        
        # Get chunks for temporal analysis
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Extract themes through different methods
        key_themes = self._identify_key_themes(clean_text)
        narrative_arcs = self._identify_narrative_arcs(chunks)
        recurring_concepts = self._identify_recurring_concepts(chunks)
        
        # Combine and prioritize themes
        themes = []
        
        # Add key themes
        themes.extend(key_themes)
        
        # Add narrative arcs
        themes.extend(narrative_arcs)
        
        # Add significant recurring concepts
        themes.extend(recurring_concepts)
        
        # Remove duplicates while preserving order
        unique_themes = []
        seen = set()
        for theme in themes:
            formatted = self._format_finding(theme)
            if formatted not in seen:
                unique_themes.append(formatted)
                seen.add(formatted)
        
        logger.info("Completed theme extraction")
        return unique_themes
    
    def _identify_key_themes(self, text: str) -> List[str]:
        """Identify key themes based on theme indicators.
        
        Args:
            text: Cleaned transcript text
            
        Returns:
            List of key themes
        """
        themes = []
        words = word_tokenize(text.lower())
        
        # Count theme indicators
        theme_counts = {
            category: sum(1 for word in words if word in indicators)
            for category, indicators in self.theme_indicators.items()
        }
        
        # Add themes that appear significantly
        for category, count in theme_counts.items():
            if count >= 2:  # Theme appears multiple times
                if category == 'growth':
                    themes.append("Personal growth and continuous learning")
                elif category == 'challenge':
                    themes.append("Navigating challenges and obstacles")
                elif category == 'change':
                    themes.append("Embracing change and transformation")
                elif category == 'purpose':
                    themes.append("Finding purpose and meaning")
                elif category == 'relationships':
                    themes.append("Building meaningful connections")
                elif category == 'achievement':
                    themes.append("Setting and achieving goals")
                elif category == 'resilience':
                    themes.append("Demonstrating resilience and persistence")
                elif category == 'authenticity':
                    themes.append("Maintaining authenticity and genuineness")
        
        return themes
    
    def _identify_narrative_arcs(self, chunks: List[tuple]) -> List[str]:
        """Identify narrative arcs across chunks.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of narrative arc themes
        """
        themes = []
        
        # Analyze sentiment progression
        sentiments = []
        for _, _, text in chunks:
            sentiment = self.text_processor.get_sentiment_scores(text)
            sentiments.append(sentiment['compound'])
        
        # Look for narrative patterns
        if len(sentiments) >= 3:
            # Check for growth arc (negative to positive)
            if sentiments[0] < 0 and sentiments[-1] > 0:
                themes.append("Journey from challenge to triumph")
            
            # Check for reflection arc (mixed sentiments)
            sentiment_range = max(sentiments) - min(sentiments)
            if sentiment_range > 1.0:
                themes.append("Reflective exploration of highs and lows")
        
        return themes
    
    def _identify_recurring_concepts(self, chunks: List[tuple]) -> List[str]:
        """Identify recurring concepts across chunks.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of recurring concept themes
        """
        themes = []
        
        # Extract key phrases from each chunk
        all_phrases = []
        for _, _, text in chunks:
            phrases = self.text_processor.get_key_phrases(text)
            all_phrases.extend(phrases)
        
        # Count phrase frequency
        phrase_counter = Counter(all_phrases)
        
        # Add frequently occurring concepts
        for phrase, count in phrase_counter.most_common(3):
            if count >= 2:  # Appears in multiple chunks
                themes.append(f"Recurring focus on {phrase}")
        
        return themes
