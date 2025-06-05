"""
Main script for the Style Profiler application.
Analyzes transcript chunks and generates a style profile.
"""

import argparse
import os
from pathlib import Path
from utils.md_loader import load_transcript

from agents.voice_agent import analyze as analyze_voice
from agents.theme_agent import analyze as analyze_theme
from agents.values_agent import analyze as analyze_values
from agents.emotional_tone_agent import analyze as analyze_emotion
from agents.relatability_agent import analyze as analyze_relatability

def main():
    parser = argparse.ArgumentParser(description="Style Profiler - Analyze speaker style from transcript")
    parser.add_argument('--transcript', required=True, help="Path to transcript markdown file")
    args = parser.parse_args()

    try:
        # Load and validate transcript
        print(f"Loading transcript from {args.transcript}")
        transcript_content, chunk_count = load_transcript(args.transcript)
        
        # Print sanity check
        print(f"[+] Loaded {chunk_count} chunks from transcript_chunks.md")
        print("[+] Confirmed only Speaker 2 content used")
        
        # Create output directory
        root_dir = Path(__file__).parent.parent
        output_dir = root_dir / "output" / "app2"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run analysis agents
        print("\nRunning analysis agents...")
        
        output = []
        output.append("# Style Profile\n")
        output.append("## voice:\n" + analyze_voice(transcript_content) + "\n")
        output.append("## themes:\n" + analyze_theme(transcript_content) + "\n")
        output.append("## values:\n" + analyze_values(transcript_content) + "\n")
        output.append("## emotional_tone:\n" + analyze_emotion(transcript_content) + "\n")
        output.append("## relatability:\n" + analyze_relatability(transcript_content))
        
        # Save style profile
        style_profile_path = output_dir / "style-profile.md"
        style_profile_path.write_text("\n".join(output), encoding='utf-8')
        
        print("\nAnalysis complete!")
        print(f"Style profile saved to: {style_profile_path}")
        
    except FileNotFoundError:
        print(f"Error: Could not find transcript file at {args.transcript}")
        raise
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main()
