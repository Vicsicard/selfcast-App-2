STEP 3 — Output Format + Realistic Example

You are implementing the Emotional Tone Agent.

The section titled "STEP 3 — Output Format + Realistic Example" defines **exactly how this agent's response must be structured**.

DO NOT ignore, summarize, or reinterpret this structure. Follow the formatting and behavior precisely.

Here's what to do:

1. **Return your results in valid markdown format**, beginning with this exact header line:
   ## emotional_tone:

2. **Follow that header with 4–6 bullet points**, written in natural language, that describe the emotional presence of the speaker.
   - Each bullet must highlight an insight about the tone, emotional delivery, or affective shift across the transcript.
   - The bullets must be directly informed by the speaker's language — but DO NOT copy speaker quotes.

3. **Your response must look exactly like the example:**
emotional_tone:
Grounded tone overall with flashes of grief and hesitation
Emotional intensity spikes when recounting moments of loss or transition
Delivery softens noticeably when discussing childhood or early mentors
Increasing clarity and empowerment as story progresses
Uses silence and long pauses to emphasize vulnerable moments

4. **Use the transcript example provided in the prompt as a guide for how to extract emotional insights.** You do not need to include this example in your actual output — it's there to teach you how to think about emotional tone.

5. **DO NOT extract values, themes, voice traits, or relatability.**
This agent is ONLY responsible for describing the *emotional arc and tone* across the transcript.
Stay completely focused on affective delivery, mood, and progression of feeling.

6. You are building a module that will be imported and called inside a pipeline. It must output a clean, stand-alone markdown string that can be saved into `style-profile.md`.

🚫 NO freeform paragraphs.  
✅ YES to structured, markdown-safe bullet points as shown.

Do not proceed to any other logic or responsibilities. This agent handles emotional tone only.
