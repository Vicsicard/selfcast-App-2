"""Relatability Assessment Agent.

Identifies connection points and shared experiences in the transcript.
"""

from typing import List, Dict, Set
from collections import Counter

from loguru import logger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

from .base import BaseAgent
from ..utils.text_processor import TextProcessor

class RelatabilityAssessor(BaseAgent):
    """Assesses relatability and connection points."""
    
    def __init__(self):
        """Initialize the relatability assessor."""
        self.text_processor = TextProcessor()
        
        # Experience categories and their indicators
        self.experience_indicators = {
            'career_change': {
                'words': {'career', 'job', 'switch', 'transition', 'industry'},
                'phrase': "Career changers navigating transitions"
            },
            'entrepreneurship': {
                'words': {'business', 'startup', 'founder', 'entrepreneur', 'launch'},
                'phrase': "Entrepreneurs building their vision"
            },
            'personal_growth': {
                'words': {'growth', 'journey', 'learn', 'develop', 'improve'},
                'phrase': "Personal growth seekers"
            },
            'leadership': {
                'words': {'lead', 'team', 'manage', 'responsibility', 'guide'},
                'phrase': "Emerging and established leaders"
            },
            'creativity': {
                'words': {'create', 'art', 'design', 'express', 'creative'},
                'phrase': "Creative professionals and artists"
            },
            'burnout': {
                'words': {'stress', 'overwhelm', 'burnout', 'balance', 'pressure'},
                'phrase': "Professionals managing work-life balance"
            }
        }
    
    def analyze(self, transcript: str) -> List[str]:
        """Identify relatability factors.
        
        Args:
            transcript: Full transcript text
            
        Returns:
            List of relatability findings as bullet points
        """
        logger.info("Starting relatability assessment")
        
        # Clean transcript
        clean_text = self._clean_transcript(transcript)
        
        # Get chunks for context analysis
        chunks = self.text_processor.extract_chunks(transcript)
        
        # Analyze through different methods
        shared_experiences = self._identify_shared_experiences(clean_text)
        connection_points = self._identify_connection_points(chunks)
        audience_alignment = self._identify_audience_alignment(chunks)
        
        # Combine findings
        findings = []
        findings.extend(shared_experiences)
        findings.extend(connection_points)
        findings.extend(audience_alignment)
        
        # Format findings
        findings = [self._format_finding(f) for f in findings]
        
        logger.info("Completed relatability assessment")
        return findings
    
    def _identify_shared_experiences(self, text: str) -> List[str]:
        """Identify common shared experiences.
        
        Args:
            text: Cleaned transcript text
            
        Returns:
            List of shared experience findings
        """
        findings = []
        words = word_tokenize(text.lower())
        
        # Check for experience indicators
        for category, data in self.experience_indicators.items():
            if any(word in words for word in data['words']):
                findings.append(data['phrase'])
        
        return findings
    
    def _identify_connection_points(self, chunks: List[tuple]) -> List[str]:
        """Identify emotional and situational connection points.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of connection point findings
        """
        findings = []
        
        # Look for universal experiences
        universal_indicators = {
            'everyone': 'Universal human experiences',
            'we all': 'Shared human challenges',
            'like you': 'Direct audience connection',
            'understand': 'Empathetic understanding'
        }
        
        # Look for struggle-to-success patterns
        struggle_indicators = {'difficult', 'struggle', 'challenge', 'hard'}
        success_indicators = {'overcome', 'succeed', 'achieve', 'accomplish'}
        
        for _, _, text in chunks:
            text_lower = text.lower()
            words = set(text_lower.split())
            
            # Check for universal connections
            for indicator, finding in universal_indicators.items():
                if indicator in text_lower:
                    findings.append(finding)
            
            # Check for relatable journey patterns
            if (any(word in words for word in struggle_indicators) and
                any(word in words for word in success_indicators)):
                findings.append("Relatable journey from struggle to success")
        
        return findings
    
    def _identify_audience_alignment(self, chunks: List[tuple]) -> List[str]:
        """Identify specific audience alignment points.
        
        Args:
            chunks: List of (chunk_id, timestamp, text) tuples
            
        Returns:
            List of audience alignment findings
        """
        findings = []
        
        # Look for specific audience indicators
        professional_indicators = {
            'corporate': 'Corporate professionals seeking change',
            'startup': 'Startup founders and entrepreneurs',
            'creative': 'Creative professionals and artists',
            'leader': 'Leaders and managers',
            'expert': 'Subject matter experts'
        }
        
        # Look for life stage indicators
        life_stage_indicators = {
            'career': 'Career transition phase',
            'growth': 'Personal development journey',
            'change': 'Major life changes',
            'build': 'Building something new'
        }
        
        # Analyze each chunk
        for _, _, text in chunks:
            text_lower = text.lower()
            
            # Check professional alignment
            for indicator, finding in professional_indicators.items():
                if indicator in text_lower:
                    findings.append(finding)
            
            # Check life stage alignment
            for indicator, finding in life_stage_indicators.items():
                if indicator in text_lower:
                    findings.append(finding)
        
        return findings
