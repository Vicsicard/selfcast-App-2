"""
Check if transcript_chunks.md exists and is readable.
"""
from pathlib import Path
import sys

def check_transcript():
    # Define expected file path
    file_path = Path("output/app2/transcript_chunks.md")
    
    # Check existence
    if not file_path.exists():
        print("Error: transcript_chunks.md not found!")
        print(f"Expected location: {file_path.absolute()}")
        sys.exit(1)
        
    # Check if it's a file
    if not file_path.is_file():
        print("Error: transcript_chunks.md exists but is not a file!")
        sys.exit(1)
        
    # Check readability
    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.strip():
            print("Warning: transcript_chunks.md is empty!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Cannot read transcript_chunks.md: {str(e)}")
        sys.exit(1)
        
    # Success
    print("✓ transcript_chunks.md exists and is readable")
    print(f"Location: {file_path.absolute()}")
    print(f"Size: {file_path.stat().st_size:,} bytes")
    
if __name__ == "__main__":
    check_transcript()
