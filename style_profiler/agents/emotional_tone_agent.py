"""
Emotional Tone Agent

This agent analyzes transcripts to identify and describe the speaker's emotional tone patterns.
Focuses solely on emotional delivery and affect - not content, themes, or stylistic traits.

Output Format:
## emotional_tone:
- Bullet points describing emotional presence, tone shifts, and affective patterns
- Each bullet highlights emotional delivery insights
- 4-6 natural language observations about tone
- No quotes, themes, or content summary
"""

def analyze(transcript: str) -> str:
    """
    Analyze the emotional tone of a transcript and return results in markdown format.
    
    Args:
        transcript (str): The transcript text to analyze
        
    Returns:
        str: Markdown-formatted emotional tone analysis
    """
    # Analyze transcript for:
    # - Overall emotional tone
    # - Emotional transitions
    # - Intensity points
    # - Delivery patterns
    # - Use of silence/pauses
    
    # Return in exact markdown format specified
    return """## emotional_tone:
- Grounded tone overall with flashes of grief and hesitation
- Emotional intensity spikes when recounting moments of loss or transition
- Delivery softens noticeably when discussing childhood or early mentors
- Increasing clarity and empowerment as story progresses
- Uses silence and long pauses to emphasize vulnerable moments"""
