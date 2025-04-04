"""
Relatability Agent identifies points of connection between Speaker 1's story and potential audiences,
focusing on shared experiences and universal struggles that create emotional resonance.
"""

from typing import List, Dict, Set
import re

def _extract_speaker_1_responses(transcript: str) -> str:
    """Extract only Speaker 1's responses from the transcript."""
    speaker_1_pattern = r'(?:^|\n)Speaker 1:([^\n]*(?:\n(?!Speaker\s*\d:)[^\n]*)*)'
    responses = []
    
    matches = re.finditer(speaker_1_pattern, transcript)
    for match in matches:
        response = match.group(1).strip()
        if response:
            responses.append(response)
    
    return ' '.join(responses)

def _find_audience_connections(text: str) -> Dict[str, Set[str]]:
    """
    Identify audience connection points based on shared experiences and struggles.
    Returns dict of connection types to sets of relevant audience descriptors.
    """
    connections = {
        'professional': set(),
        'emotional': set(),
        'life_stage': set(),
        'identity': set()
    }
    
    # Professional resonance patterns
    if re.search(r'(?i)job|career|title|award|success|work|profession|industry', text):
        if re.search(r'(?i)burn(?:ed|t)?[\s-]out|exhaust(?:ed|ion)|overwhelm(?:ed)?', text):
            connections['professional'].add('professionals facing burnout')
        if re.search(r'(?i)achieve|perform|excel|accomplish|standard|expect', text):
            connections['professional'].add('high-achieving professionals')
        if re.search(r'(?i)change|transition|pivot|quit|left|move|switch', text):
            connections['professional'].add('career changers')
            connections['life_stage'].add('people in career transition')
    
    # Emotional resonance patterns
    if re.search(r'(?i)hide|mask|pretend|fake|smile|appear', text):
        connections['emotional'].add('people hiding their struggles')
    if re.search(r'(?i)empty|hollow|unfulfill|meaning|purpose', text):
        connections['emotional'].add('seekers of authentic purpose')
    if re.search(r'(?i)fear|afraid|worry|anxiety|stress|pressure', text):
        connections['emotional'].add('individuals under pressure to conform')
    
    # Life stage resonance patterns
    if re.search(r'(?i)start[\s-]over|begin|again|new|fresh|change', text):
        connections['life_stage'].add('people starting over')
    if re.search(r'(?i)later|after|finally|now|time', text):
        connections['life_stage'].add('late bloomers')
    if re.search(r'(?i)break(?:down)?|crisis|rock[\s-]bottom|collapse', text):
        connections['life_stage'].add('those recovering from breakdowns')
    
    # Identity resonance patterns
    if re.search(r'(?i)real|authentic|true|genuine|actually', text):
        connections['identity'].add('seekers of authenticity')
    if re.search(r'(?i)creative|artist|maker|build|create|express', text):
        connections['identity'].add('creatives')
    if re.search(r'(?i)different|unique|special|outsider|alone', text):
        connections['identity'].add('people feeling different or misunderstood')
    
    return connections

def _find_universal_struggles(text: str) -> Set[str]:
    """
    Identify universal emotional struggles that create connection points.
    """
    struggles = set()
    
    patterns = [
        (r'(?i)invisible|unseen|overlooked|ignored', 'feelings of invisibility'),
        (r'(?i)too\s+(?:much|little|big|small|loud|quiet)', 'fear of being "too much" or "not enough"'),
        (r'(?i)should|must|have\s+to|expected', 'pressure to meet expectations'),
        (r'(?i)real|truth|authentic|genuine', 'desire for authenticity'),
        (r'(?i)alone|lonely|isolated|different', 'feelings of isolation'),
        (r'(?i)change|transform|become|evolve', 'journey of transformation')
    ]
    
    for pattern, struggle in patterns:
        if re.search(pattern, text):
            struggles.add(struggle)
    
    return struggles

def analyze(transcript: str) -> str:
    """
    Analyze relatability factors from Speaker 1's responses, focusing on audience
    connection points where readers may see themselves reflected.
    
    Args:
        transcript (str): The full transcript text
        
    Returns:
        str: Markdown-formatted relatability analysis
    """
    speaker_text = _extract_speaker_1_responses(transcript)
    
    # Find audience connections and universal struggles
    connections = _find_audience_connections(speaker_text)
    struggles = _find_universal_struggles(speaker_text)
    
    # Build resonance points
    resonance_points = []
    
    # Add professional and identity connections
    prof_identity = connections['professional'].union(connections['identity'])
    if prof_identity:
        resonance_points.append(f"Will resonate with {', '.join(prof_identity)}")
    
    # Add emotional struggles
    if struggles:
        resonance_points.append(f"Story includes universal {', '.join(list(struggles)[:3])}")
    
    # Add life stage connections
    life_stage = connections['life_stage']
    if life_stage:
        resonance_points.append(f"Speaks to {', '.join(life_stage)}")
    
    # Add emotional connections
    emotional = connections['emotional']
    if emotional:
        resonance_points.append(f"Connects with {', '.join(emotional)}")
    
    # Format output
    output = ["## Relatability Analysis"]
    for point in resonance_points:
        output.append(f"- {point}")
    
    return "\n".join(output)
