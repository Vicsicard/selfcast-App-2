"""
Main script for the Style Profiler application.
"""

import argparse
from utils.md_loader import load_transcript

from agents.voice_agent import analyze as voice_analyze
from agents.theme_agent import analyze as theme_analyze
from agents.values_agent import analyze as values_analyze
from agents.emotional_tone_agent import analyze as emotion_analyze
from agents.relatability_agent import analyze as relatability_analyze

def main():
    parser = argparse.ArgumentParser(description="Style Profiler - Analyze speaker style from transcript")
    parser.add_argument('--transcript', required=True, help="Path to transcript markdown file")
    args = parser.parse_args()

    # Load transcript
    transcript = load_transcript(args.transcript)

    # Generate profile sections
    output = "# style-profile.md\n\n"
    output += voice_analyze(transcript) + "\n"
    output += theme_analyze(transcript) + "\n"
    output += values_analyze(transcript) + "\n"
    output += emotion_analyze(transcript) + "\n"
    output += relatability_analyze(transcript) + "\n"

    # Save output
    with open("style-profile.md", "w", encoding="utf-8") as f:
        f.write(output)
        
    print(f"Style profile saved to: style-profile.md")

if __name__ == "__main__":
    main()
