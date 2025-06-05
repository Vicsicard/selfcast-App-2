#!/usr/bin/env python
"""
Transfer files from App 2 to App 3 format in Supabase.
This script takes the output files from App 2 and uploads them to Supabase
in the structure expected by App 3.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

def get_supabase_headers():
    """Get standard headers for Supabase API requests."""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

def upload_file_to_supabase(bucket_name, file_path, target_path, content=None):
    """Upload a file to Supabase storage.
    
    Args:
        bucket_name: Name of the storage bucket
        file_path: Path to local file to upload
        target_path: Target path in Supabase storage
        content: File content (if already loaded)
        
    Returns:
        bool: True if successful, False otherwise
    """
    headers = get_supabase_headers()
    headers["Content-Type"] = "application/octet-stream"
    
    # Load file content if not provided
    if content is None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return False
    
    # Upload to Supabase
    try:
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{bucket_name}/{target_path}"
        response = requests.post(
            upload_url,
            headers=headers,
            data=content
        )
        
        if response.status_code not in (200, 201):
            print(f"Error uploading to {target_path}: {response.text}")
            return False
            
        print(f"Successfully uploaded to {bucket_name}/{target_path}")
        return True
        
    except Exception as e:
        print(f"Error uploading to {target_path}: {str(e)}")
        return False

def transfer_files_to_app3_format(display_name, output_dir):
    """Transfer files from App 2 to App 3 format in Supabase.
    
    Args:
        display_name: Display name for the client
        output_dir: Directory with App 2 output files
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Convert display name to client_id format (lowercase, hyphens)
    client_id = display_name.lower().replace(' ', '-')
    
    # Locate App 2 output files
    output_dir = Path(output_dir)
    style_profile_path = output_dir / "style-profile.md"
    chunk_scores_path = output_dir / "video_chunk_scores.json"
    
    if not style_profile_path.exists():
        print(f"Error: style-profile.md not found in {output_dir}")
        return False
        
    if not chunk_scores_path.exists():
        print(f"Error: video_chunk_scores.json not found in {output_dir}")
        return False
    
    # Define target paths in Supabase (App 3 format)
    base_path = f"client-files/{client_id}"
    style_profile_target = f"{base_path}/style-profile.md"
    
    # Upload style profile
    print(f"Transferring files for client '{client_id}':")
    success = upload_file_to_supabase(
        bucket_name="content",
        file_path=style_profile_path,
        target_path=style_profile_target
    )
    
    if not success:
        return False
    
    # Also upload chunk scores for reference
    chunk_scores_target = f"{base_path}/video_chunk_scores.json"
    success = upload_file_to_supabase(
        bucket_name="content",
        file_path=chunk_scores_path,
        target_path=chunk_scores_target
    )
    
    if not success:
        print("Warning: Failed to upload chunk scores, but continuing...")
    
    # Find transcript from App 1 and upload it as well
    app1_transcript_path = None
    
    # Check for transcript in App 2's input folder first
    possible_app1_transcript = Path("input") / display_name / f"{display_name}.md"
    if possible_app1_transcript.exists():
        app1_transcript_path = possible_app1_transcript
    else:
        # Try input folder directly
        input_dir = Path("input")
        for folder in input_dir.glob("*"):
            if folder.is_dir() and display_name.lower().replace(' ', '') in folder.name.lower().replace(' ', ''):
                md_files = list(folder.glob("*.md"))
                if md_files:
                    app1_transcript_path = md_files[0]
                    break
                    
        # Also look for transcript in App 1's completed_transcripts folder
        if not app1_transcript_path:
            app1_dir = Path("..") / "self-cast-studio-app-1" / "completed_transcripts"
            if app1_dir.exists():
                # Check if any folder contains our display name (with various possible transformations)
                display_name_variants = [
                    display_name.lower(),
                    display_name.lower().replace(' ', ''),
                    display_name.lower().replace(' ', '-'),
                    ''.join(c for c in display_name.lower() if c.isalnum())
                ]
                
                for folder in app1_dir.glob("*"):
                    if folder.is_dir():
                        folder_name_lower = folder.name.lower()
                        # Check if any variant matches any part of the folder name
                        if any(variant in folder_name_lower for variant in display_name_variants):
                            # Check for .md files in this folder
                            md_files = list(folder.glob("*.md"))
                            if md_files:
                                app1_transcript_path = md_files[0]
                                print(f"Found transcript match in App 1 folder: {folder}")
                                break
    
    if app1_transcript_path:
        print(f"Found transcript: {app1_transcript_path}")
        transcript_target = f"{base_path}/transcript_chunks.md"
        success = upload_file_to_supabase(
            bucket_name="content",
            file_path=app1_transcript_path,
            target_path=transcript_target
        )
        
        if not success:
            print("Error: Failed to upload transcript")
            return False
    else:
        print("Error: Could not find transcript file from App 1")
        return False
    
    # All files uploaded successfully!
    print("\nAll files transferred successfully!")
    print(f"Client ID for App 3: {client_id}")
    print(f"\nTo run App 3 with these files, use:")
    print(f"python -m content_generator.content_generator --client {client_id}")
    
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Transfer App 2 files to App 3 format in Supabase")
    parser.add_argument("--name", required=True, help="Display name (e.g., 'Annie New 5-2-25-GG')")
    parser.add_argument("--output", default="output", help="Output directory with App 2 files")
    
    args = parser.parse_args()
    
    # Verify Supabase credentials
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env file")
        sys.exit(1)
    
    # Transfer files
    success = transfer_files_to_app3_format(args.name, args.output)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
