# Style Profiler App 2 - PRD
*Last Updated: April 11, 2025*

## Overview
The Style Profiler App 2 analyzes markdown transcripts to extract and document an author's unique stylistic and narrative characteristics. The output guides AI content generation to maintain authentic voice, tone, and style consistency.

## Core Functionality
- Processes markdown transcript files containing workshop interview responses
- Employs five specialized AI agents for multi-faceted analysis
- Generates a structured style profile document
- Supports both CLI and modular integration

## Technical Specifications

### Input
- **Primary**: `transcript_chunks.md` file
  - Contains workshop interview responses
  - Structured with question headers and timestamps
  - Speaker 1 responses grouped by workshop questions
- **Optional**: CLI configuration flags
  - `--transcript`: Custom file path specification

### Output
- **File**: `style-profile.md`
- **Format**: Structured markdown with five analysis sections:
  1. Voice characteristics
  2. Recurring themes
  3. Core values
  4. Emotional tone patterns
  5. Relatability factors

### AI Agent Architecture
Five independent analysis agents, each:
- Focuses solely on Speaker 1 content
- Operates within a specific analytical domain
- Produces markdown-formatted output
- Maintains consistent output structure
- Ensures human readability

## Quality Requirements
- Complete section generation (all 5 components)
- Fact-based analysis (no content hallucination)
- Modular agent design
- CLI functionality
- Downstream compatibility (App 3 integration)

## Scalability Considerations
- Supports client-specific style library creation
- Future expansion possibilities:
  - Version control integration
  - Differential analysis
  - Interactive feedback mechanisms
  - Agent enhancement capabilities

## Implementation Notes
- Each agent operates independently
- Analysis confined to provided transcript content
- Standardized markdown output format
- Designed for pipeline integration
- Built for maintainability and extensibility
