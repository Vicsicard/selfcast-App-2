"""Values Identification Agent.

Identifies core principles and beliefs from the transcript.
"""

from typing import List, Dict, Set
from collections import Counter

from loguru import logger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

from .base import BaseAgent
from ..utils.text_processor import TextProcessor

class ValuesIdentifier(BaseAgent):
    """Identifies core values and principles."""
    
    def __init__(self):
        """Initialize the values identifier."""
        self.text_processor = TextProcessor()
        
        # Value-related keywords and their categories
        self.value_indicators = {
            'integrity': {
                'words': {'honest', 'truth', 'integrity', 'authentic', 'genuine'},
                'phrase': "Values authenticity and truth"
            },
            'growth': {
                'words': {'learn', 'grow', 'improve', 'develop', 'progress'},
                'phrase': "Commitment to continuous growth"
            },
            'courage': {
                'words': {'brave', 'courage', 'bold', 'risk', 'fear'},
                'phrase': "Embraces courage over comfort"
            },
            'creativity': {
                'words': {'create', 'innovate', 'imagine', 'original', 'unique'},
                'phrase': "Prioritizes creative expression"
            },
            'connection': {
                'words': {'connect', 'relationship', 'community', 'together', 'share'},
                'phrase': "Values meaningful connections"
            },
            'autonomy': {
                'words': {'freedom', 'independent', 'choice', 'decide', 'control'},
                'phrase': "Prizes personal autonomy"
            },
            'impact': {
                'words': {'impact', 'difference', 'change', 'help', 'serve'},
                'phrase': "Driven by meaningful impact"
            },
            'excellence': {
                'words': {'quality', 'excellence', 'best', 'standard', 'perfect'},
                'phrase': "Strives for excellence"
            }
        }
    
    def analyze(self, transcript: str) -> List[str]:
        """Identify core values from the transcript.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of identified values as bullet points
        """
        logger.info("Starting values identification")
        
        # Clean transcript
        clean_text = self._clean_transcript(transcript)
        
        # Get chunks for context analysis
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Analyze through different methods
        explicit_values = self._identify_explicit_values(clean_text)
        implicit_values = self._identify_implicit_values(chunks)
        priority_values = self._identify_priority_values(chunks)
        
        # Combine all values
        values = []
        values.extend(explicit_values)
        values.extend(implicit_values)
        values.extend(priority_values)
        
        # Remove duplicates while preserving order
        unique_values = []
        seen = set()
        for value in values:
            formatted = self._format_finding(value)
            if formatted not in seen:
                unique_values.append(formatted)
                seen.add(formatted)
        
        logger.info("Completed values identification")
        return unique_values
    
    def _identify_explicit_values(self, text: str) -> List[str]:
        """Identify explicitly stated values.
        
        Args:
            text: Cleaned transcript text
            
        Returns:
            List of explicit values
        """
        values = []
        words = word_tokenize(text.lower())
        
        # Check for value indicators
        for category, data in self.value_indicators.items():
            if any(word in words for word in data['words']):
                values.append(data['phrase'])
        
        return values
    
    def _identify_implicit_values(self, chunks: List[tuple]) -> List[str]:
        """Identify values implied through behavior and choices.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of implicit values
        """
        values = []
        
        # Look for decision patterns
        decision_indicators = {
            'chose', 'decided', 'picked', 'selected', 'opted'
        }
        
        # Look for priority indicators
        priority_indicators = {
            'important', 'matters', 'priority', 'believe', 'must'
        }
        
        for _, _, text in chunks:
            words = word_tokenize(text.lower())
            
            # Check for decisions
            if any(word in words for word in decision_indicators):
                # Analyze the context
                if 'right' in words or 'truth' in words:
                    values.append("Chooses integrity over convenience")
                if 'hard' in words or 'difficult' in words:
                    values.append("Values growth over comfort")
            
            # Check for priorities
            if any(word in words for word in priority_indicators):
                if 'people' in words or 'others' in words:
                    values.append("Prioritizes human connection")
                if 'quality' in words or 'excellence' in words:
                    values.append("Values excellence in craft")
        
        return values
    
    def _identify_priority_values(self, chunks: List[tuple]) -> List[str]:
        """Identify values through prioritization patterns.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of priority-based values
        """
        values = []
        
        # Look for "over" statements indicating clear priorities
        for _, _, text in chunks:
            sentences = sent_tokenize(text.lower())
            
            for sentence in sentences:
                # Look for "X over Y" patterns
                if ' over ' in sentence:
                    if 'truth' in sentence or 'honest' in sentence:
                        values.append("Truth over comfort")
                    if 'quality' in sentence or 'excellence' in sentence:
                        values.append("Quality over quantity")
                    if 'purpose' in sentence or 'meaning' in sentence:
                        values.append("Purpose over profit")
                    if 'learn' in sentence or 'grow' in sentence:
                        values.append("Growth over stability")
        
        return values
