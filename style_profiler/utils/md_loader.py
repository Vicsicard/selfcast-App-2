"""
Markdown file loader and parser utility.
"""

def load_transcript(filepath: str) -> str:
    """
    Load a markdown transcript file.
    
    Args:
        filepath (str): Path to the markdown transcript file
        
    Returns:
        str: Raw content of the markdown transcript
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file encoding is not UTF-8
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def extract_speaker_content(content: str) -> str:
    """
    Extract only Speaker 1's content from the transcript.
    
    Args:
        content (str): Raw markdown content
        
    Returns:
        str: Filtered content containing only Speaker 1's responses
    """
    # TODO: Implement speaker content extraction
    return content
