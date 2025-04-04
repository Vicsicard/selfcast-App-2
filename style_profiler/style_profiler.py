"""
Main script for the Style Profiler application.
"""

import argparse
import os
import shutil
from utils.md_loader import load_transcript
from utils.supabase_loader import get_chunks_for_user_project

from agents.voice_agent import analyze as analyze_voice
from agents.theme_agent import analyze as analyze_theme
from agents.values_agent import analyze as analyze_values
from agents.emotional_tone_agent import analyze as analyze_emotion
from agents.relatability_agent import analyze as analyze_relatability

def main():
    parser = argparse.ArgumentParser(description="Style Profiler - Analyze speaker style from transcript")
    parser.add_argument('--transcript', required=True, help="Path to transcript markdown file")
    parser.add_argument('--project-id', help="Project ID for Supabase query")
    parser.add_argument('--user-id', help="User ID for Supabase query")
    args = parser.parse_args()

    # Load local markdown transcript
    transcript = load_transcript(args.transcript)

    # Load Supabase chunks if IDs provided
    has_supabase = False
    if args.project_id and args.user_id:
        chunks = get_chunks_for_user_project(args.project_id, args.user_id)
        has_supabase = True
        print(f"✅ Loaded {len(chunks)} chunks from Supabase for user {args.user_id} / project {args.project_id}")

    # Analyze transcript with agents
    output = "## voice\n" + analyze_voice(transcript) + "\n"
    output += "## themes\n" + analyze_theme(transcript) + "\n"
    output += "## values\n" + analyze_values(transcript) + "\n"
    output += "## emotional_tone\n" + analyze_emotion(transcript) + "\n"
    output += "## relatability\n" + analyze_relatability(transcript)

    # Get project root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Save style profile
    style_profile_path = os.path.join(root_dir, "style-profile.md")
    with open(style_profile_path, "w", encoding="utf-8") as f:
        f.write(output)

    # Create export directory for App 3
    export_dir = os.path.join(root_dir, "output", "for_app3")
    os.makedirs(export_dir, exist_ok=True)

    # Copy files to export directory
    shutil.copy2(style_profile_path, os.path.join(export_dir, "style-profile.md"))
    
    transcript_chunks_path = os.path.join(root_dir, "..", "transcript_builder", "output", "transcript_chunks.md")
    if os.path.exists(transcript_chunks_path):
        shutil.copy2(transcript_chunks_path, os.path.join(export_dir, "transcript_chunks.md"))
        
    print("✅ style_profile.md generated")
    print("📦 Transcript source: [Local]")
    if has_supabase:
        print("🧠 Metadata source: [Supabase]")
        
    print("\n✅ App 3 Handoff Ready")
    print("📦 Files copied to: /output/for_app3/")
    print("📁 Includes:")
    print("- transcript_chunks.md")
    print("- style-profile.md")

if __name__ == "__main__":
    main()
