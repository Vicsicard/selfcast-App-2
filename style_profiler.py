#!/usr/bin/env python
"""Style Profiler - Main entry point.

Analyzes interview transcripts to extract stylistic and narrative fingerprints.
Generates structured profiles and chunk-level scoring for transcript analysis.
Supports both Supabase (legacy) and MongoDB storage backends.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from loguru import logger
from dotenv import load_dotenv

# Import agents
from src.agents.voice import VoiceAnalyzer
from src.agents.theme import ThemeExtractor
from src.agents.values import ValuesIdentifier
from src.agents.emotional import EmotionalToneAnalyzer
from src.agents.relatability import RelatabilityAssessor

# Import scoring
from src.scoring.scorer import ChunkScorer

# Load environment variables
load_dotenv()

# Conditionally import storage backends
use_mongodb = os.environ.get('USE_MONGODB', 'false').lower() == 'true'

# Import the appropriate storage backend
if use_mongodb:
    from src.utils.mongodb_client import (
        store_style_profile,
        MongoDBError as StorageError,
        MongoDBConfigError as ConfigError,
        MongoDBConnectionError as ConnectionError,
        MongoDBQueryError as QueryError
    )
    logger.info("Using MongoDB storage backend")
else:
    from src.utils.supabase_client import (
        store_style_profile,
        SupabaseError as StorageError,
        SupabaseConfigError as ConfigError,
        SupabaseStorageError as ConnectionError,
        SupabaseDatabaseError as QueryError
    )
    logger.info("Using Supabase storage backend (legacy)")

def setup_logging(output_dir: Path) -> None:
    """Configure logging settings.
    
    Args:
        output_dir: Directory for log files
    """
    # Remove default logger
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        level="INFO"
    )
    
    # Add file handler
    log_file = output_dir / "style_profiler.log"
    logger.add(
        log_file,
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True
    )
    
    logger.info(f"Logging configured. Log file: {log_file}")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze transcripts to extract stylistic and narrative fingerprints."
    )
    parser.add_argument(
        "--transcript",
        type=str,
        help="Path to the transcript_chunks.md file"
    )
    parser.add_argument(
        "--project-id",
        type=str,
        help="Project ID for storage"
    )
    parser.add_argument(
        "--client-id",
        type=str,
        help="Client ID for storage"
    )
    parser.add_argument(
        "--display-name",
        type=str,
        help="Display name for the client"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory (default: output/)"
    )
    parser.add_argument(
        "--mongodb",
        action="store_true",
        help="Use MongoDB instead of Supabase"
    )
    parser.add_argument(
        "--job-id",
        type=str,
        help="Job ID for API server mode"
    )
    
    args = parser.parse_args()
    
    # Validate required arguments
    if not args.transcript and not args.client_id:
        parser.error("Either --transcript or --client-id must be provided")
    
    # Set MongoDB flag in environment
    if args.mongodb:
        os.environ['USE_MONGODB'] = 'true'
        global use_mongodb
        use_mongodb = True
        logger.info("MongoDB storage backend enabled via command line")
    
    return args

def load_transcript(transcript_path: str) -> str:
    """Load and validate the transcript file.
    
    Args:
        transcript_path: Path to the transcript file
        
    Returns:
        str: Content of the transcript file
        
    Raises:
        FileNotFoundError: If transcript file doesn't exist
        ValueError: If transcript file is empty
    """
    path = Path(transcript_path)
    if not path.exists():
        error_msg = f"Transcript file not found: {transcript_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    content = path.read_text(encoding="utf-8")
    if not content:
        error_msg = f"Transcript file is empty: {transcript_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"Successfully loaded transcript from {transcript_path}")
    logger.debug(f"Transcript size: {len(content)} characters")
    return content

def analyze_transcript(transcript: str) -> Dict[str, Any]:
    """Run all analysis agents on the transcript.
    
    Args:
        transcript: Content of the transcript file
        
    Returns:
        Dict[str, Any]: Analysis results from all agents
    """
    logger.info("Starting transcript analysis...")
    
    try:
        # Initialize agents
        voice_analyzer = VoiceAnalyzer()
        theme_extractor = ThemeExtractor()
        values_identifier = ValuesIdentifier()
        emotional_analyzer = EmotionalToneAnalyzer()
        relatability_assessor = RelatabilityAssessor()
        
        # Run analysis
        profile = {
            "voice": voice_analyzer.analyze(transcript),
            "themes": theme_extractor.analyze(transcript),
            "values": values_identifier.analyze(transcript),
            "emotional_tone": emotional_analyzer.analyze(transcript),
            "relatability": relatability_assessor.analyze(transcript)
        }
        
        # Log analysis stats
        for section, items in profile.items():
            logger.debug(f"{section} analysis: {len(items)} findings")
        
        logger.info("Transcript analysis completed successfully")
        return profile
        
    except Exception as e:
        error_msg = f"Error during transcript analysis: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

def generate_profile_markdown(profile: Dict[str, Any], output_dir: Path) -> str:
    """Generate the style-profile.md file.
    
    Args:
        profile: Analysis results from all agents
        output_dir: Directory to save the markdown file
        
    Returns:
        str: The generated markdown content
    """
    try:
        content = [
            "# Style Profile",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        ]
        
        # Add each section
        for section, items in profile.items():
            content.extend([
                f"## {section}:",
                *[f"- {item}" for item in items],
                ""  # Empty line between sections
            ])
        
        # Join content into a single string
        markdown_content = "\n".join(content)
        
        # Save locally
        output_path = output_dir / "style-profile.md"
        output_path.write_text(markdown_content, encoding="utf-8")
        logger.info(f"Generated style profile: {output_path}")
        logger.debug(f"Profile size: {len(markdown_content)} characters")
        
        return markdown_content
        
    except Exception as e:
        error_msg = f"Error generating markdown profile: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

def load_transcript_from_mongodb(client_id: str, project_id: Optional[str] = None) -> str:
    """Load transcript chunks from MongoDB.
    
    Args:
        client_id: The client's UUID
        project_id: Optional project ID
        
    Returns:
        str: Combined transcript content
        
    Raises:
        ValueError: If transcript cannot be found
    """
    try:
        # Import here to avoid circular imports
        from src.utils.mongodb_client import get_transcript_chunks
        
        # Get transcript chunks
        chunks_data = get_transcript_chunks(client_id)
        
        if not chunks_data or not chunks_data.get('chunks'):
            error_msg = f"No transcript chunks found for client {client_id}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Combine chunks into a single transcript
        chunks = chunks_data['chunks']
        chunks.sort(key=lambda x: x.get('order', 0))
        
        transcript = "\n\n".join([chunk.get('content', '') for chunk in chunks])
        
        logger.info(f"Successfully loaded transcript from MongoDB for client {client_id}")
        logger.debug(f"Transcript size: {len(transcript)} characters")
        
        return transcript
        
    except Exception as e:
        error_msg = f"Error loading transcript from MongoDB: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e

def update_job_status(job_id: str, status: str, error: Optional[str] = None) -> None:
    """Update job status in the job metadata file.
    
    Args:
        job_id: The job ID
        status: New status
        error: Optional error message
    """
    try:
        if not job_id:
            return
            
        job_dir = Path(f"output/{job_id}")
        if not job_dir.exists():
            logger.warning(f"Job directory not found: {job_dir}")
            return
            
        metadata_file = job_dir / "job_metadata.json"
        if not metadata_file.exists():
            logger.warning(f"Job metadata file not found: {metadata_file}")
            return
            
        # Read current metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            
        # Update status and timestamp
        metadata['status'] = status
        metadata['updated_at'] = datetime.utcnow().isoformat()
        
        if error:
            metadata['error'] = error
            
        # Write updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        logger.info(f"Updated job status to {status} for job {job_id}")
        
    except Exception as e:
        logger.error(f"Error updating job status: {str(e)}")

def main() -> None:
    """Main entry point."""
    exit_code = 0
    job_id = None
    
    try:
        # Parse arguments
        args = parse_args()
        job_id = args.job_id
        
        # Set up output directory
        if job_id:
            output_dir = Path(f"output/{job_id}")
        else:
            output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        setup_logging(output_dir)
        
        logger.info("Style Profiler starting...")
        logger.info(f"Arguments: {args}")
        
        # Update job status if in API mode
        if job_id:
            update_job_status(job_id, "processing")
        
        # Load transcript - either from file or MongoDB
        if args.transcript:
            transcript = load_transcript(args.transcript)
        elif args.client_id:
            transcript = load_transcript_from_mongodb(args.client_id, args.project_id)
        else:
            raise ValueError("No transcript source specified")
        
        # Analyze transcript
        profile = analyze_transcript(transcript)
        
        # Generate markdown profile
        markdown_profile = generate_profile_markdown(profile, output_dir)
        
        # Score chunks for analysis
        chunk_scorer = ChunkScorer()
        chunk_scores = chunk_scorer.score_chunks(transcript, profile)
        
        # Save scores to file
        scores_file = output_dir / "chunk_scores.json"
        with open(scores_file, "w", encoding="utf-8") as f:
            json.dump(chunk_scores, f, indent=2)
        logger.info(f"Saved chunk scores to {scores_file}")
        
        # Store profile in the database
        try:
            # Get display name
            display_name = args.display_name
            if not display_name:
                display_name = f"Client-{args.client_id[:8] if args.client_id else args.project_id}"
            
            # Store profile
            result = store_style_profile(display_name, profile, chunk_scores)
            logger.info(f"Stored style profile in MongoDB: {result}")
            
            # Update job status if in API mode
            if job_id:
                update_job_status(job_id, "completed")
            
        except (ConfigError, ConnectionError, QueryError) as e:
            error_msg = f"Storage error: {str(e)}"
            logger.error(error_msg)
            
            # Update job status if in API mode
            if job_id:
                update_job_status(job_id, "failed", error_msg)
            
            # Continue execution - local files are still generated
        
        logger.info("Style Profiler completed successfully")
        
    except Exception as e:
        error_msg = f"Unhandled error: {str(e)}"
        logger.exception(error_msg)
        
        # Update job status if in API mode
        if job_id:
            update_job_status(job_id, "failed", error_msg)
            
        exit_code = 1
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
