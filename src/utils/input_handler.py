"""Input handling and validation for transcript files."""

import json
from pathlib import Path
from typing import Dict, Any, Tuple

from loguru import logger

class InputHandler:
    """Handles loading and validation of input files."""
    
    def __init__(self, transcript_path: str):
        """Initialize the input handler.
        
        Args:
            transcript_path: Path to transcript_chunks.md file
        """
        self.transcript_path = Path(transcript_path)
        self.base_dir = self.transcript_path.parent
        
    def validate_and_load(self) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
        """Validate and load all required input files.
        
        Returns:
            Tuple of (transcript_text, chunk_metadata, video_index)
            
        Raises:
            FileNotFoundError: If any required file is missing
            ValueError: If any file is empty or invalid
        """
        # Check transcript file
        if not self.transcript_path.exists():
            raise FileNotFoundError(f"Transcript file not found: {self.transcript_path}")
            
        # Load transcript
        transcript_text = self.transcript_path.read_text(encoding="utf-8")
        if not transcript_text:
            raise ValueError(f"Transcript file is empty: {self.transcript_path}")
            
        # Validate transcript format
        if not self._validate_transcript_format(transcript_text):
            raise ValueError(f"Invalid transcript format: {self.transcript_path}")
            
        # Load metadata
        chunk_metadata = self._load_json("annie_chunk_metadata.json")
        video_index = self._load_json("annie_video_index.json")
        
        logger.info("Successfully loaded and validated all input files")
        return transcript_text, chunk_metadata, video_index
    
    def _validate_transcript_format(self, text: str) -> bool:
        """Validate the transcript file format.
        
        Args:
            text: Transcript text to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # Check for required elements
        required_elements = [
            "## [Chunk",  # Chunk headers
            "**Timestamp**:",  # Timestamps
            "> Speaker 2:"  # Speaker markers
        ]
        
        return all(element in text for element in required_elements)
    
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Load and validate a JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Parsed JSON content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or invalid JSON
        """
        file_path = self.base_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not data:
                raise ValueError(f"Empty JSON file: {file_path}")
                
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")
