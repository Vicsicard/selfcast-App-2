# Style Profiler (App 2)

Analyzes interview transcripts to extract stylistic and narrative fingerprints, generating structured profiles and chunk-level scoring for transcript analysis. Part of the Self Cast Studios workflow pipeline.

## Requirements

- Python 3.10 ONLY
- Virtual environment (venv310)
- MongoDB database (primary storage)
- Supabase project (legacy support)

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
Copy `.env.example` to `.env` and fill in your credentials:
```
# MongoDB (primary storage)
MONGODB_URI=mongodb+srv://username:password@cluster0.example.mongodb.net/database-name?retryWrites=true&w=majority
USE_MONGODB=true

# Supabase (legacy support)
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# API Server
API_KEY=your_secure_api_key
PORT=5000
APP3_WEBHOOK_URL=https://app3-url/webhook/endpoint
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
│       ├── mongodb_client.py # MongoDB integration
│       ├── supabase_client.py # Supabase integration (legacy)
│       └── text_processor.py  # Text processing
├── api_server.py        # API server for webhook integration
├── notify_app3.py       # Notification script for App 3
├── render.yaml          # Render deployment configuration
└── tests/              # Unit tests
```

## Usage

### Command Line Usage

1. Place your transcript file in the input directory:
```bash
cp path/to/transcript_chunks.md input/
```

2. Run the style profiler with MongoDB:
```bash
python style_profiler.py --transcript input/transcript_chunks.md --project-id your_project_id --client-id your_client_id --mongodb
```

Or with Supabase (legacy):
```bash
python style_profiler.py --transcript input/transcript_chunks.md --project-id your_project_id
```

This will:
- Generate a style profile (style-profile.md)
- Score transcript chunks (chunk_scores.json)
- Store results in MongoDB or Supabase

### API Server Usage

1. Start the API server:
```bash
python api_server.py
```

2. Send a webhook request to process a transcript:
```bash
curl -X POST http://localhost:5000/webhook/process-transcript \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{"projectId":"your_project_id","clientId":"your_client_id","displayName":"Client Name"}'
```

3. Check job status:
```bash
curl -X GET http://localhost:5000/jobs/your_job_id \
  -H "Authorization: Bearer your_api_key"
```

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

## Storage Integration

### MongoDB (Primary)

Results are stored in these collections:
- `clients`: Client information
- `projects`: Project metadata
- `transcript_chunks`: Transcript content
- `style_profiles`: Style analysis results
- `processing_tasks`: Job status tracking

### Supabase (Legacy)

Results are also stored in (for backward compatibility):
- Storage bucket: "documents"
- Table: "transcript_files"
- Paths: `{project_id}/style-profile.md` and `{project_id}/chunk_scores.json`

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

## Deployment on Render

This application is configured for deployment on Render using the `render.yaml` file:

1. Push code to a Git repository
2. Connect repository to Render
3. Create a new Web Service using the Blueprint
4. Environment variables will be automatically configured

The deployment includes:
- API server for webhook integration
- MongoDB connection
- Automatic notification to App 3 when processing completes

## Integration with Self Cast Studios Pipeline

This app is part of the Self Cast Studios workflow:

1. App 1 (Transcript Builder) sends a webhook to this app when a transcript is ready
2. This app (Style Profiler) processes the transcript and generates style profiles
3. When complete, this app notifies App 3 (Content Generator) to continue the workflow

The complete pipeline flow is:
```
Vapi → Unified → App 1 (Transcript Builder) → App 2 (Style Profiler) → App 3 (Content Generator) → Marketing Automation
```

## License

Copyright 2025 Self Cast Studios. All rights reserved.
