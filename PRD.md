PRD: style_profiler App2
App Purpose:
 Analyze a markdown transcript file (transcript_chunks.md) and extract the author's stylistic and narrative fingerprint into a structured file called style-profile.md. This file will guide all future AI-generated content to ensure voice, tone, and authenticity are preserved.

🧩 1. What the App Does
Accepts a .md transcript (Speaker 1 responses grouped by workshop questions)


Uses five AI “agents” to independently extract:


Voice


Themes


Values


Emotional Tone


Relatability


Each agent generates a markdown-formatted section


The app combines those sections into one unified file: style-profile.md



🛠 2. Inputs
transcript_chunks.md: A full markdown transcript of a workshop interview, structured as:


md
CopyEdit
## [Q04] Turning Point  
**Matched Question**: What’s a time you had to change direction in your life?  
**Timestamp**: 00:04:22 — 00:07:10  
> Speaker 1: I knew something had to give…  
> Speaker 1: I was just surviving, not living.

Optional: CLI flags for --transcript file path



📤 3. Outputs
style-profile.md
 Markdown file containing five sections:


md
CopyEdit
## voice:
- Calm, reflective tone
- Often uses metaphors or analogies...

## themes:
- Reinvention, identity shift, control vs surrender...

## values:
- Truth over comfort, authenticity, loyalty...

## emotional_tone:
- Empathetic, hopeful, with undercurrents of grief...

## relatability:
- Late bloomers, high-achievers in burnout, career changers...


🧠 4. Agent Logic Summary
Each Tier 2 agent must:
Analyze only the Speaker 1 content


Interpret narrative features through a clear lens


Return its section as valid markdown with a header + bullets


Output must be human-readable and consistent across transcripts



🧪 5. Success Criteria
✅ style-profile.md is created with all 5 sections
 ✅ No hallucination of facts — all content derived from speaker responses
 ✅ Agents run independently, and are importable as modules
 ✅ CLI usable locally or integrated into future pipelines
 ✅ Easily passed into downstream content generators (App 3)

📦 6. Scalability Notes
Will be used to create style libraries per client


May later include versioning or diff checks between style profiles


Possible upgrade: each agent can support feedback loop editing

