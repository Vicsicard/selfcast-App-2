# Style Profiler

A tool that analyzes markdown transcripts to extract the author's stylistic and narrative fingerprint.

## Overview

Style Profiler processes workshop interview transcripts and generates a structured style profile that captures:
- Voice characteristics
- Recurring themes
- Core values
- Emotional tone
- Relatability factors

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and configure as needed

## Usage

```bash
python style_profiler.py path/to/transcript_chunks.md
```

The tool will generate a `style-profile.md` file containing the analysis results.

## Project Structure

```
style_profiler/
├── agents/               # Analysis agents
│   ├── voice_agent.py
│   ├── theme_agent.py
│   ├── values_agent.py
│   ├── emotional_tone_agent.py
│   └── relatability_agent.py
├── utils/               # Utility functions
│   └── md_loader.py
├── style_profiler.py    # Main script
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## Input Format

The input transcript should be a markdown file structured as:

```markdown
## [Q04] Turning Point  
**Matched Question**: What's a time you had to change direction in your life?  
**Timestamp**: 00:04:22 — 00:07:10  
> Speaker 1: I knew something had to give…  
> Speaker 1: I was just surviving, not living.
```

## Output Format

The generated `style-profile.md` will contain sections for:
- Voice analysis
- Theme analysis
- Values analysis
- Emotional tone analysis
- Relatability analysis
