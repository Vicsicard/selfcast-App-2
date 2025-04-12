✅ UPDATED PRD
 🟪 SELF CAST STUDIOS – APP 2: STYLE PROFILER
 Module 2 of 6 → Refined to align with updated App 1 transcript output

🎯 App Purpose
 Analyze a markdown transcript file (transcript_chunks.md) that includes only Speaker 2 responses. Extract the subject’s stylistic and narrative fingerprint into a structured file called style-profile.md.
This file guides all future AI-generated content to ensure tone, authenticity, and personal narrative are preserved across platforms. Additionally, App 2 generates numerical scores per chunk to support intelligent video selection in App 4.

🧩 1. What the App Does
Accepts a clean markdown transcript of Speaker 2 responses only, broken into timestamped narrative chunks


Runs five independent agents to extract:


Voice


Themes


Values


Emotional Tone (with score)


Relatability (with score)


Each agent outputs one markdown-formatted section


A sixth module generates a video_chunk_scores.json file that scores each chunk based on:


Emotional tone intensity


Relatability strength


Theme labels (tags)



🛠 2. Inputs
transcript_chunks.md: Markdown transcript file, where each chunk includes:


## [Chunk 06]  
**Timestamp**: 00:11:30 — 00:12:04  
> Speaker 2: I kept showing up, even when I had no idea what I was doing. That persistence changed everything.

Each chunk contains only Speaker 2’s words


No question prompts, no speaker filtering required


Optional CLI flags:
--transcript path/to/transcript_chunks.md



📤 3. Outputs
style-profile.md: A markdown file containing five consistently formatted sections:


## voice:
- Calm, reflective, measured delivery
- Uses metaphor and personal storytelling

## themes:
- Navigating change with intention
- Reframing failure as opportunity

## values:
- Authenticity over perfection
- Loyalty to one’s inner compass

## emotional_tone:
- Gritty optimism, occasional grief, grounded wisdom

## relatability:
- Career changers seeking purpose
- High-performers who hit burnout and bounced back

video_chunk_scores.json: Chunk-level scoring data for App 4


{
  "chunk_06": {
    "emotional_tone_score": 0.91,
    "relatability_score": 0.88,
    "theme_tags": ["resilience", "reinvention"]
  },
  "chunk_07": {
    "emotional_tone_score": 0.65,
    "relatability_score": 0.92,
    "theme_tags": ["self-doubt"]
  }
}


🧠 4. Agent Logic Summary
Each Tier 2 agent must:
Analyze all Speaker 2 chunks in aggregate


Infer narrative meaning and stylistic traits solely from the subject’s responses


Return a bullet-point list formatted in valid markdown (for style-profile.md)


For scoring:
A sixth logic module processes each individual chunk


Assigns emotional_tone_score and relatability_score between 0.00–1.00


Labels each chunk with inferred theme_tags


Saves output to video_chunk_scores.json



🧪 5. Success Criteria
✅ style-profile.md is successfully created with all 5 narrative dimensions
 ✅ video_chunk_scores.json is created with scoring for all chunks
 ✅ Scores are based on speaker text only, no hallucination
 ✅ Output is human-readable and markdown-valid
 ✅ All six agents/modules are modular, reusable, and CLI-compatible
 ✅ Compatible with downstream apps (App 3 – Content Generator, App 4 – Reel Selector)

📦 6. Scalability Notes
Profile files will be versioned per subject/client


Chunk scoring supports App 4’s autonomous reel selection


May be expanded with feedback loop editing and user ranking


Possible future traits: pacing, speaking quirks, narrative arc shape



This updated PRD reflects your streamlined interview flow — no reliance on question prompts, full focus on authentic self-expression, and downstream compatibility with content and media workflows.


# Style Profiler App 2 - v1.1
*Updated: April 11, 2025*

## 🎯 Overview
Style Profiler v1.1 analyzes Speaker 2's narrative from transcript chunks to generate a comprehensive style profile using five specialized AI agents. Each agent focuses on a specific narrative dimension, producing structured markdown output that captures the speaker's authentic voice and style.

## 🔄 Version Changes (v1.1)
- Streamlined to process Speaker 2-only transcripts
- Removed question prompt dependencies
- Enhanced chunk processing for better narrative flow
- Improved integration with App 1 output format

## 📋 Implementation Steps

### Step 1: Input Handling
#### Requirements
- Load `transcript_chunks.md` from `/output/` directory
- Process Speaker 2-only narrative chunks
- Parse timestamp and content structure

#### Input Format
```markdown
## [Chunk 06]  
**Timestamp**: 00:11:30 — 00:12:04  
> Speaker 2: I kept showing up, even when I had no idea what I was doing...
```

#### Validation Checks
- File exists in `/output/` directory
- Valid markdown formatting
- Contains only Speaker 2 content
- Proper chunk structure with timestamps

### Step 2: Analysis Agents
#### Core Requirements
- Each agent operates independently
- Analyzes complete Speaker 2 content
- Generates fact-based findings only (no hallucinations)
- Returns structured markdown section
- Uses consistent bullet-point format

#### Agent Specifications

| Agent | Purpose | Section Header | Analysis Focus |
|-------|---------|---------------|----------------|
| 1. Voice Analysis | Speaking style and patterns | `## voice:` | Delivery, word choice, pacing |
| 2. Theme Extraction | Central narratives | `## themes:` | Story arcs, recurring concepts |
| 3. Values Identification | Core principles | `## values:` | Beliefs, priorities, non-negotiables |
| 4. Emotional Tone | Emotional patterns | `## emotional_tone:` | Sentiment, intensity, transitions |
| 5. Relatability | Connection points | `## relatability:` | Shared experiences, audience alignment |

#### Output Format Example
```markdown
## values:
- Truth over comfort
- Loyalty to one's inner compass
- Creative freedom as a non-negotiable
```

#### Agent Processing Rules
1. **Data Isolation**
   - Each agent processes transcript independently
   - No cross-agent data sharing during analysis
   - Results combined only in final output

2. **Analysis Scope**
   - Consider full transcript context
   - Identify patterns across all chunks
   - Weight recurring elements appropriately

3. **Output Standards**
   - Use consistent bullet-point formatting
   - Keep findings concise and specific
   - Maintain uniform markdown structure

4. **Validation Requirements**
   - All findings must link to transcript content
   - No speculative or inferred content
   - Clear evidence for each bullet point

#### Integration Points
- Input: Processed transcript chunks from Step 1
- Output: Individual markdown sections
- Combination: All sections merged into final style-profile.md

### Step 3: Output Generation
#### Output File Specifications
- **Path**: `/output/app2/style-profile.md`
- **Format**: Valid markdown
- **Encoding**: UTF-8
- **Line Endings**: LF (Unix-style)

#### File Structure
```markdown
# Style Profile
Generated: [Timestamp]

## voice:
[Voice Analysis Agent output]

## themes:
[Theme Extraction Agent output]

## values:
[Values Identification Agent output]

## emotional_tone:
[Emotional Tone Agent output]

## relatability:
[Relatability Assessment Agent output]
```

#### Processing Requirements
1. **Section Assembly**
   - Collect output from all 5 agents
   - Maintain section order as specified
   - Preserve bullet-point formatting
   - Ensure consistent spacing between sections

2. **Validation Checks**
   - Verify all 5 sections are present
   - Confirm valid markdown syntax
   - Check for proper bullet-point formatting
   - Validate UTF-8 encoding

3. **Directory Management**
   - Create `/output/app2/` if not exists
   - Handle file overwrite scenarios
   - Set appropriate file permissions

4. **Downstream Compatibility**
   - Ensure parseable by App 3 (Content Generator)
   - Maintain consistent section headers
   - Follow markdown best practices
   - Include metadata for version tracking

#### Error Handling
- Log missing sections
- Report markdown validation issues
- Handle file system errors
- Provide detailed error messages

#### Success Indicators
- File created at correct path
- All sections present and properly formatted
- Valid markdown structure
- Readable by downstream applications
- Proper UTF-8 encoding

### Step 4: Success Validation

#### Required Checks
| Validation | Description | Status |
|------------|-------------|---------|
| File Existence | `style-profile.md` exists in output directory | Required |
| Section Completeness | All 5 sections present and properly formatted | Required |
| Header Validation | Correct section headers used (`## voice:`, etc.) | Required |
| Content Source | Analysis based solely on Speaker 2 content | Required |
| Markdown Validity | Valid markdown syntax throughout file | Required |

#### Technical Requirements
1. **Dependencies**
   - No video/audio processing required
   - No database connections needed
   - Text-only analysis

2. **CLI Implementation**
```bash
python style_profiler.py --transcript path/to/transcript_chunks.md
```

#### Command Line Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| --transcript | Yes | Path to input transcript file |
| --output | No | Custom output directory (default: /output/app2/) |
| --help | No | Show help message and exit |

#### Validation Process
1. **Pre-execution Checks**
   - Verify input file exists
   - Confirm input file is valid markdown
   - Check output directory permissions

2. **Runtime Validation**
   - Monitor agent execution status
   - Track section generation progress
   - Validate markdown formatting

3. **Output Verification**
   - Confirm file creation
   - Verify all sections present
   - Check section header format
   - Validate content source

#### Error Handling
- Clear error messages for missing files
- Input format validation errors
- Section generation failures
- File permission issues

⚠️ **Important Notes**
- Operates on text content only
- No external service dependencies
- No database operations
- Designed for CLI execution
- Focus on markdown processing

## 🎯 Success Criteria
- Clean input processing of Speaker 2 content
- Accurate section generation by all 5 agents
- Valid markdown output format
- Integration with App 1 output structure
- Preparation for App 3 (Content Generator) input

## 📦 Technical Notes
- Input Path: `/output/transcript_chunks.md`
- Output Path: `/output/style-profile.md`
- Format: Markdown
- Dependencies: App 1 transcript format

## 🔄 Next Steps
1. Implement input validation
2. Develop agent processing pipeline
3. Set up output formatting
4. Add error handling
5. Test with App 1 output samples

## 📋 Implementation Checklist

### 1. Input Processing
- [ ] Load transcript_chunks.md from /output/
- [ ] Filter for Speaker 2 content only
- [ ] Preserve chunk timestamps
- [ ] Validate input file format
- [ ] Handle missing/malformed files

### 2. Agent Implementation
| Agent | Implementation | Output Section | Content Quality |
|-------|---------------|----------------|-----------------|
| Voice Analysis | [ ] Complete | [ ] Present | [ ] 2-3+ bullets |
| Theme Extraction | [ ] Complete | [ ] Present | [ ] 2-3+ bullets |
| Values Identification | [ ] Complete | [ ] Present | [ ] 2-3+ bullets |
| Emotional Tone | [ ] Complete | [ ] Present | [ ] 2-3+ bullets |
| Relatability | [ ] Complete | [ ] Present | [ ] 2-3+ bullets |

### 3. Output Verification
#### File Generation
- [ ] Creates /output/app2/ directory
- [ ] Generates style-profile.md
- [ ] Uses correct file path
- [ ] Valid markdown syntax

#### Content Validation
- [ ] All 5 sections present
- [ ] Correct section order
- [ ] Minimum 2-3 bullets per section
- [ ] No hallucinated content
- [ ] Grounded in transcript text

### 4. CLI Implementation
#### Basic Functionality
- [ ] Runs via `python style_profiler.py --transcript <path>`
- [ ] Accepts custom output path
- [ ] Provides help documentation
- [ ] Returns success confirmation

#### Error Handling
- [ ] Invalid file path
- [ ] Malformed input file
- [ ] Missing sections
- [ ] Permission issues
- [ ] Resource constraints

### 5. Technical Requirements
#### Dependencies
- [ ] No video processing
- [ ] No audio processing
- [ ] No database connections
- [ ] No external APIs required

#### Logging
- [ ] Console output for status
- [ ] Error reporting to stdout
- [ ] Progress indicators
- [ ] Completion confirmation

## 🔍 Final Verification
Before marking complete, verify:
1. All checklist items addressed
2. No external dependencies
3. Clean CLI execution
4. Valid output generation
5. Proper error handling
6. Complete documentation

## 📊 Testing Matrix
| Test Case | Expected Result | Status |
|-----------|----------------|---------|
| Valid input | Generate complete profile | [ ] |
| Missing file | Error message | [ ] |
| Empty file | Error message | [ ] |
| Bad format | Error message | [ ] |
| No Speaker 2 | Error message | [ ] |
| Success case | Console confirmation | [ ] |
