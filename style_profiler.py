#!/usr/bin/env python
"""Style Profiler - Main entry point.

Analyzes interview transcripts to extract stylistic and narrative fingerprints.
Generates structured profiles and chunk-level scoring for video selection.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from loguru import logger

# Import agents
from src.agents.voice import VoiceAnalyzer
from src.agents.theme import ThemeExtractor
from src.agents.values import ValuesIdentifier
from src.agents.emotional import EmotionalToneAnalyzer
from src.agents.relatability import RelatabilityAssessor

# Import scoring and storage
from src.scoring.scorer import ChunkScorer
from src.utils.supabase_client import (
    store_style_profile,
    SupabaseError,
    SupabaseConfigError,
    SupabaseStorageError,
    SupabaseDatabaseError
)

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
        required=True,
        help="Path to the transcript_chunks.md file"
    )
    parser.add_argument(
        "--project-id",
        type=str,
        required=True,
        help="Project ID for Supabase storage"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory (default: output/)"
    )
    return parser.parse_args()

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

def main() -> None:
    """Main entry point."""
    exit_code = 0
    
    try:
        # Parse arguments
        args = parse_args()
        
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        setup_logging(output_dir)
        logger.info("Starting Style Profiler")
        logger.info(f"Project ID: {args.project_id}")
        
        try:
            # Load and analyze transcript
            transcript = load_transcript(args.transcript)
            profile = analyze_transcript(transcript)
            
            # Generate outputs
            profile_content = generate_profile_markdown(profile, output_dir)
            
            # Score chunks
            logger.info("Starting chunk scoring...")
            scorer = ChunkScorer()
            scores = scorer.score_chunks(transcript)
            logger.info(f"Scored {len(scores)} chunks")
            
            # Save chunk scores locally
            scores_path = output_dir / "video_chunk_scores.json"
            with open(scores_path, "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=2)
            logger.info(f"Saved chunk scores to {scores_path}")
            
            # Store results in Supabase
            logger.info("Storing results in Supabase...")
            store_style_profile(args.project_id, profile_content, scores)
            logger.info("Successfully stored results in Supabase")
            
            logger.info("Style Profiler completed successfully")
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            exit_code = 1
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            exit_code = 1
        except SupabaseConfigError as e:
            logger.error(f"Supabase configuration error: {str(e)}")
            exit_code = 1
        except SupabaseStorageError as e:
            logger.error(f"Supabase storage error: {str(e)}")
            exit_code = 1
        except SupabaseDatabaseError as e:
            logger.error(f"Supabase database error: {str(e)}")
            exit_code = 1
        except SupabaseError as e:
            logger.error(f"Supabase error: {str(e)}")
            exit_code = 1
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            exit_code = 1
            
    except Exception as e:
        logger.exception(f"Critical error: {str(e)}")
        exit_code = 1
        
    finally:
        if exit_code != 0:
            logger.error("Style Profiler failed")
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
