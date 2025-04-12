"""Text processing utilities for analysis agents."""

import re
from typing import List, Dict, Tuple

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class TextProcessor:
    """Utility class for text processing operations."""
    
    def __init__(self):
        """Initialize the text processor."""
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def extract_chunks(self, transcript: str) -> List[Tuple[str, str, str]]:
        """Extract chunks from the transcript.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of tuples (chunk_id, timestamp, text)
        """
        chunks = []
        current_chunk = []
        chunk_id = ""
        timestamp = ""
        
        for line in transcript.split("\n"):
            if line.startswith("## [Chunk"):
                # Save previous chunk if exists
                if current_chunk and chunk_id:
                    chunks.append((
                        chunk_id,
                        timestamp,
                        "\n".join(current_chunk)
                    ))
                # Start new chunk
                chunk_id = line.strip("[] \n")
                current_chunk = []
            elif line.startswith("**Timestamp**:"):
                timestamp = line.replace("**Timestamp**:", "").strip()
            elif line.startswith("> Speaker 2:"):
                current_chunk.append(
                    line.replace("> Speaker 2:", "").strip()
                )
        
        # Add final chunk
        if current_chunk and chunk_id:
            chunks.append((chunk_id, timestamp, "\n".join(current_chunk)))
        
        return chunks
    
    def get_sentiment_scores(self, text: str) -> Dict[str, float]:
        """Get sentiment scores for text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of sentiment scores
        """
        return self.sentiment_analyzer.polarity_scores(text)
    
    def get_key_phrases(self, text: str, top_n: int = 5) -> List[str]:
        """Extract key phrases from text.
        
        Args:
            text: Text to analyze
            top_n: Number of phrases to return
            
        Returns:
            List of key phrases
        """
        # Tokenize and tag parts of speech
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)
        
        # Extract noun phrases (simple approach)
        phrases = []
        current_phrase = []
        
        for word, tag in tagged:
            if tag.startswith(('JJ', 'NN')):  # Adjectives and nouns
                if word not in self.stop_words:
                    current_phrase.append(word)
            else:
                if current_phrase:
                    phrases.append(" ".join(current_phrase))
                    current_phrase = []
        
        # Add final phrase
        if current_phrase:
            phrases.append(" ".join(current_phrase))
        
        # Return top phrases by frequency
        phrase_freq = {}
        for phrase in phrases:
            if len(phrase.split()) > 1:  # Only multi-word phrases
                phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1
        
        return sorted(
            phrase_freq.keys(),
            key=lambda x: phrase_freq[x],
            reverse=True
        )[:top_n]
    
    def get_speaking_style(self, text: str) -> Dict[str, float]:
        """Analyze speaking style metrics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of style metrics
        """
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        tagged = pos_tag(words)
        
        # Calculate metrics
        avg_sentence_len = len(words) / len(sentences)
        question_ratio = sum(1 for s in sentences if s.endswith('?')) / len(sentences)
        
        # Count word types
        word_types = {
            'adjectives': sum(1 for _, tag in tagged if tag.startswith('JJ')),
            'adverbs': sum(1 for _, tag in tagged if tag.startswith('RB')),
            'first_person': sum(1 for w in words if w.lower() in {'i', 'me', 'my', 'mine', 'myself'})
        }
        
        return {
            'avg_sentence_length': avg_sentence_len,
            'question_ratio': question_ratio,
            'word_types': word_types
        }
