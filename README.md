# Style Profiler (App 2)

Analyzes interview transcripts to extract stylistic and narrative fingerprints, generating structured profiles and chunk-level scoring for video selection.

## Requirements

- Python 3.10 ONLY
- Virtual environment (venv310)
- Supabase project with storage buckets and database tables

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv310
.\venv310\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```bash
python download_nltk.py
```

4. Configure environment:
Copy `.env.example` to `.env` and fill in your Supabase credentials:
```
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## Directory Structure

```
/
├── input/                 # Source transcript files
├── output/               # Generated profiles and scores
├── src/
│   ├── agents/          # Analysis agents
│   │   ├── base.py     # Base agent class
│   │   ├── voice.py    # Voice analysis
│   │   ├── theme.py    # Theme extraction
│   │   ├── values.py   # Values identification
│   │   ├── emotional.py # Emotional tone analysis
│   │   └── relatability.py # Relatability assessment
│   ├── scoring/         # Chunk scoring
│   │   └── scorer.py   # ChunkScorer class
│   └── utils/          # Utilities
│       ├── supabase_client.py # Supabase integration
│       └── text_processor.py  # Text processing
└── tests/              # Unit tests
```

## Usage

1. Place your transcript file in the input directory:
```bash
cp path/to/transcript_chunks.md input/
```

2. Run the style profiler:
```bash
python style_profiler.py --transcript input/transcript_chunks.md --project-id your_project_id
```

This will:
- Generate a style profile (style-profile.md)
- Score video chunks (video_chunk_scores.json)
- Store results in Supabase

## Output Files

1. Style Profile (`style-profile.md`):
   - Voice characteristics
   - Key themes
   - Core values
   - Emotional tone
   - Relatability factors

2. Chunk Scores (`video_chunk_scores.json`):
   - Emotional tone scores (0.0-1.0)
   - Relatability scores (0.0-1.0)
   - Theme tags

## Supabase Integration

Results are stored in:
- Storage bucket: "documents"
- Table: "transcript_files"
- Paths: `{project_id}/style-profile.md` and `{project_id}/video_chunk_scores.json`

## Error Handling

The script provides:
- Detailed error messages
- Colored console output
- Debug logs in output/style_profiler.log
- Exit codes for automation

## Contributing

1. Create feature branch
2. Make changes
3. Run tests: `python -m pytest tests/`
4. Submit pull request

## License

Copyright 2025 Codeium. All rights reserved.
