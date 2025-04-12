"""Voice Analysis Agent.

Analyzes speaking style and patterns in the transcript.
"""

from typing import List
import statistics
from collections import Counter

from loguru import logger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

from .base import BaseAgent
from ..utils.text_processor import TextProcessor

class VoiceAnalyzer(BaseAgent):
    """Analyzes speaking style, word choice, and delivery patterns."""
    
    def __init__(self):
        """Initialize the voice analyzer."""
        self.text_processor = TextProcessor()
        
    def analyze(self, transcript: str) -> List[str]:
        """Analyze speaking style and patterns.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of voice characteristics as bullet points
        """
        logger.info("Starting voice analysis")
        
        # Clean transcript
        clean_text = self._clean_transcript(transcript)
        
        # Get chunks for temporal analysis
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Analyze different aspects
        style_metrics = self.text_processor.get_speaking_style(clean_text)
        pacing = self._analyze_pacing(chunks)
        word_choices = self._analyze_word_choices(clean_text)
        delivery = self._analyze_delivery(chunks)
        
        # Compile findings
        findings = []
        
        # Add style characteristics
        if style_metrics['avg_sentence_length'] > 20:
            findings.append("Uses detailed, expansive sentences")
        else:
            findings.append("Favors concise, direct communication")
            
        if style_metrics['word_types']['first_person'] > 10:
            findings.append("Speaks from personal experience")
            
        if style_metrics['word_types']['adjectives'] > 30:
            findings.append("Highly descriptive speaking style")
            
        # Add pacing insights
        findings.extend(pacing)
        
        # Add word choice patterns
        findings.extend(word_choices)
        
        # Add delivery patterns
        findings.extend(delivery)
        
        # Format all findings
        findings = [self._format_finding(f) for f in findings]
        
        logger.info("Completed voice analysis")
        return findings
    
    def _analyze_pacing(self, chunks: List[tuple]) -> List[str]:
        """Analyze speaking pace and rhythm.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of pacing-related findings
        """
        findings = []
        
        # Analyze sentence lengths per chunk
        lengths = []
        for _, _, text in chunks:
            sentences = sent_tokenize(text)
            if sentences:
                lengths.append(len(sentences))
        
        if lengths:
            avg_length = statistics.mean(lengths)
            if avg_length > 3:
                findings.append("Tends to elaborate with multiple connected thoughts")
            else:
                findings.append("Delivers ideas in focused, discrete segments")
        
        return findings
    
    def _analyze_word_choices(self, text: str) -> List[str]:
        """Analyze word choice patterns.
        
        Args:
            text: Cleaned transcript text
            
        Returns:
            List of word choice findings
        """
        findings = []
        
        # Get POS tags
        words = word_tokenize(text.lower())
        tagged = pos_tag(words)
        
        # Analyze metaphors and imagery
        metaphor_indicators = ['like', 'as', 'imagine', 'picture']
        if any(word in words for word in metaphor_indicators):
            findings.append("Uses metaphors and imagery to illustrate points")
        
        # Check for technical language
        technical_indicators = sum(1 for w, t in tagged if t.startswith('NN') and len(w) > 8)
        if technical_indicators > 5:
            findings.append("Comfortable with technical/specialized vocabulary")
        
        return findings
    
    def _analyze_delivery(self, chunks: List[tuple]) -> List[str]:
        """Analyze delivery patterns.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of delivery-related findings
        """
        findings = []
        
        # Analyze question frequency
        questions = sum(1 for _, _, text in chunks if '?' in text)
        if questions > len(chunks) * 0.2:
            findings.append("Engages through rhetorical questions")
        
        # Analyze emphasis patterns
        emphasis = sum(1 for _, _, text in chunks if '!' in text)
        if emphasis > len(chunks) * 0.1:
            findings.append("Uses dynamic emphasis for key points")
        else:
            findings.append("Maintains measured, even-keeled delivery")
        
        return findings
