"""Base agent class for all analysis agents."""

from abc import ABC, abstractmethod
from typing import List

class BaseAgent(ABC):
    """Base class for all analysis agents."""
    
    @abstractmethod
    def analyze(self, transcript: str) -> List[str]:
        """Analyze the transcript and return findings.
        
        Args:
            transcript: The full transcript text to analyze
            
        Returns:
            List of findings as bullet points
        """
        pass
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean the transcript text for analysis.
        
        Args:
            transcript: Raw transcript text
            
        Returns:
            Cleaned transcript text
        """
        # Remove timestamps and chunk headers
        lines = []
        for line in transcript.split("\n"):
            if line.startswith("> Speaker 2:"):
                # Extract just the spoken text
                lines.append(line.replace("> Speaker 2:", "").strip())
        
        return " ".join(lines)
    
    def _format_finding(self, finding: str) -> str:
        """Format a finding as a bullet point.
        
        Args:
            finding: Raw finding text
            
        Returns:
            Formatted bullet point
        """
        # Remove any existing bullet points or dashes
        finding = finding.lstrip("*-• ").strip()
        
        # Ensure first letter is capitalized
        if finding and finding[0].isalpha():
            finding = finding[0].upper() + finding[1:]
            
        return finding
