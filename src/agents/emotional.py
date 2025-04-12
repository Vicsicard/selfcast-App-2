"""Emotional Tone Analysis Agent.

Analyzes emotional patterns and sentiment in the transcript.
"""

from typing import List, Dict, Tuple
import statistics
from collections import Counter

from loguru import logger
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

from .base import BaseAgent
from ..utils.text_processor import TextProcessor

class EmotionalToneAnalyzer(BaseAgent):
    """Analyzes emotional tone and sentiment patterns."""
    
    def __init__(self):
        """Initialize the emotional tone analyzer."""
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Emotion categories and their indicators
        self.emotion_indicators = {
            'joy': {'happy', 'excited', 'love', 'wonderful', 'amazing'},
            'optimism': {'hope', 'believe', 'positive', 'better', 'future'},
            'determination': {'will', 'must', 'determined', 'committed', 'decided'},
            'reflection': {'think', 'realize', 'understand', 'learned', 'know'},
            'concern': {'worried', 'concerned', 'afraid', 'fear', 'anxious'},
            'gratitude': {'thankful', 'grateful', 'appreciate', 'blessed', 'luck'}
        }
    
    def analyze(self, transcript: str) -> List[str]:
        """Analyze emotional tone patterns.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of emotional tone characteristics as bullet points
        """
        logger.info("Starting emotional tone analysis")
        
        # Clean transcript
        clean_text = self._clean_transcript(transcript)
        
        # Get chunks for temporal analysis
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Analyze through different methods
        overall_tone = self._analyze_overall_tone(clean_text)
        emotional_patterns = self._analyze_emotional_patterns(chunks)
        transitions = self._analyze_emotional_transitions(chunks)
        
        # Combine findings
        findings = []
        findings.extend(overall_tone)
        findings.extend(emotional_patterns)
        findings.extend(transitions)
        
        # Format findings
        findings = [self._format_finding(f) for f in findings]
        
        logger.info("Completed emotional tone analysis")
        return findings
    
    def _analyze_overall_tone(self, text: str) -> List[str]:
        """Analyze the overall emotional tone.
        
        Args:
            text: Cleaned transcript text
            
        Returns:
            List of overall tone findings
        """
        findings = []
        
        # Get overall sentiment
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        # Interpret sentiment scores
        if sentiment['compound'] > 0.5:
            findings.append("Predominantly optimistic and positive outlook")
        elif sentiment['compound'] > 0.2:
            findings.append("Generally hopeful with balanced perspective")
        elif sentiment['compound'] > -0.2:
            findings.append("Measured and pragmatic emotional tone")
        else:
            findings.append("Reflective and growth-focused perspective")
        
        # Check emotional variety
        if sentiment['neu'] > 0.7:
            findings.append("Maintains composed, even-keeled emotional state")
        if sentiment['pos'] > 0.3 and sentiment['neg'] > 0.1:
            findings.append("Comfortable expressing full range of emotions")
        
        return findings
    
    def _analyze_emotional_patterns(self, chunks: List[tuple]) -> List[str]:
        """Analyze patterns in emotional expression.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of emotional pattern findings
        """
        findings = []
        
        # Track emotions per chunk
        chunk_emotions = []
        for _, _, text in chunks:
            # Get emotions in this chunk
            emotions = set()
            words = set(text.lower().split())
            
            for emotion, indicators in self.emotion_indicators.items():
                if any(word in words for word in indicators):
                    emotions.add(emotion)
            
            chunk_emotions.append(emotions)
        
        # Analyze patterns
        all_emotions = [e for chunk in chunk_emotions for e in chunk]
        emotion_counts = Counter(all_emotions)
        
        # Add findings based on dominant emotions
        if emotion_counts['optimism'] > len(chunks) * 0.3:
            findings.append("Consistently optimistic undertone")
        if emotion_counts['reflection'] > len(chunks) * 0.3:
            findings.append("Deeply reflective and self-aware")
        if emotion_counts['determination'] > len(chunks) * 0.2:
            findings.append("Strong sense of determination")
        if emotion_counts['gratitude'] > len(chunks) * 0.1:
            findings.append("Expresses genuine gratitude")
        
        return findings
    
    def _analyze_emotional_transitions(self, chunks: List[tuple]) -> List[str]:
        """Analyze emotional transitions between chunks.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of transition-related findings
        """
        findings = []
        
        # Track sentiment changes
        sentiments = []
        for _, _, text in chunks:
            score = self.sentiment_analyzer.polarity_scores(text)['compound']
            sentiments.append(score)
        
        if len(sentiments) >= 3:
            # Calculate sentiment changes
            changes = [abs(b - a) for a, b in zip(sentiments[:-1], sentiments[1:])]
            avg_change = statistics.mean(changes)
            
            # Interpret transitions
            if avg_change > 0.5:
                findings.append("Dynamic emotional range with clear transitions")
            elif avg_change > 0.3:
                findings.append("Natural emotional flow with gentle transitions")
            else:
                findings.append("Consistent emotional stability throughout")
            
            # Check for resolution
            if sentiments[-1] > 0 and min(sentiments) < 0:
                findings.append("Demonstrates emotional resilience and growth")
        
        return findings
