"""
Markdown file loader and parser utility.
"""
from typing import Tuple

def load_transcript(filepath: str) -> Tuple[str, int]:
    """
    Load a markdown transcript file.
    
    Args:
        filepath (str): Path to the markdown transcript file
        
    Returns:
        Tuple[str, int]: (filtered content, number of chunks)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file encoding is not UTF-8
    """
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return extract_speaker_content(content)

def extract_speaker_content(content: str) -> Tuple[str, int]:
    """
    Extract only Speaker 2's content from the transcript.
    
    Args:
        content (str): Raw markdown content
        
    Returns:
        Tuple[str, int]: (filtered content, number of chunks)
    """
    lines = content.split('\n')
    included_lines = []
    current_chunk = []
    in_speaker2_block = False
    chunk_count = 0
    
    for line in lines:
        # Start of a new chunk
        if line.startswith('## [Chunk'):
            # Save previous chunk if it had Speaker 2 content
            if current_chunk and in_speaker2_block:
                included_lines.extend(current_chunk)
                chunk_count += 1
            current_chunk = [line]
            in_speaker2_block = False
            continue
            
        # Add timestamp line if in a chunk
        if line.startswith('**Timestamp'):
            current_chunk.append(line)
            continue
            
        # Check for Speaker 2's lines
        if line.startswith('> Speaker 2:'):
            in_speaker2_block = True
            current_chunk.append(line)
            continue
            
        # Include continuation lines from Speaker 2
        if in_speaker2_block and line.startswith('>'):
            current_chunk.append(line)
            continue
            
        # Empty lines within a chunk
        if in_speaker2_block and not line.strip():
            current_chunk.append(line)
            
    # Don't forget the last chunk
    if current_chunk and in_speaker2_block:
        included_lines.extend(current_chunk)
        chunk_count += 1
        
    return '\n'.join(included_lines), chunk_count
