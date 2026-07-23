import os
import json
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert academic lab report writer and engineering educator with 20+ years of experience in physics, chemistry, electronics, and applied sciences. You write rigorous, publication-quality lab reports that follow IEEE and standard university academic formats.

Your reports must:
- Be analytically precise and scientifically accurate
- Include proper error analysis and percentage error calculations when theoretical values are given
- Use correct SI units, significant figures, and scientific notation where appropriate
- Identify and explain potential sources of systematic and random error
- Suggest genuinely useful, specific improvements to methodology (not generic advice)
- Follow strict academic writing conventions

Format your output in clean Markdown with proper headings (##, ###), bold key terms, and structured tables where appropriate."""


def build_prompt(data: dict) -> str:
    return f"""Generate a complete, professionally structured lab report from the following experimental data.

EXPERIMENT DETAILS:
- Title: {data.get('title', 'N/A')}
- Subject/Course: {data.get('subject', 'N/A')}
- Date Conducted: {data.get('date', 'N/A')}
- Student Name: {data.get('student_name', 'N/A')}

OBJECTIVE / AIM:
{data.get('objective', 'N/A')}

HYPOTHESIS:
{data.get('hypothesis', 'Not provided')}

APPARATUS & MATERIALS:
{data.get('apparatus', 'Not specified')}

EXPERIMENTAL PROCEDURE (as described by student):
{data.get('procedure', 'Not provided')}

RAW EXPERIMENTAL DATA (tabular):
{data.get('raw_data', 'No data table provided')}

OBSERVATIONS:
{data.get('observations', 'Not provided')}

THEORETICAL / STANDARD VALUES (for error analysis):
{data.get('theoretical_values', 'Not provided')}

---

Generate a complete, submission-ready lab report with ALL of the following sections. Each section must be substantive and specific to the data provided above — never generic filler.

## [Experiment Title]

## Abstract
150–200 word summary covering: objective, methodology, key results (with actual numbers from the data), and main conclusion. Must be self-contained.

## 1. Introduction
Background theory and scientific context. Why this experiment matters. Historical or practical relevance.

## 2. Theory & Governing Equations
Relevant physical/chemical/engineering principles. Key equations with variable definitions. Any derivations needed to understand the experiment.

## 3. Apparatus & Materials
Formatted list with estimated specifications. Note any critical instrument precision.

## 4. Experimental Procedure
Refined, step-by-step procedure (numbered). More precise and complete than the student's raw description.

## 5. Observations & Raw Data
Present the provided data in clean, properly labelled Markdown tables. Add column headers with units. If multiple trials exist, include them.

## 6. Data Analysis & Calculations
- Show all key calculations with working
- Calculate mean values, standard deviation if multiple trials
- If theoretical values provided: calculate percentage error for each measurement using: % Error = |(Experimental − Theoretical) / Theoretical| × 100%
- Identify which measurements have the highest error and briefly explain why

## 7. Results
Present final computed results clearly. Use a summary table. State numerical findings with proper units and significant figures.

## 8. Discussion
- Compare results to theoretical values or expected behaviour
- Analyse sources of error (distinguish systematic vs. random errors)
- Explain any anomalies in the data
- Comment on reliability and reproducibility of the method

## 9. Conclusion
Concise summary (3–5 sentences). State whether the objective was achieved and whether the hypothesis was supported. Quantify the conclusion where possible.

## 10. Methodology Improvements
Provide exactly 5 specific, actionable improvements. Each must be concrete (name specific equipment, techniques, or protocols), not vague advice like "be more careful." Explain why each improvement would reduce error or increase reliability.

## 11. Safety & Precautions
List precautions that were or should be observed. Flag any hazards specific to this experiment.

## 12. References
Suggest 3–4 relevant, real references (textbooks or standards) appropriate to this experiment's subject matter. Use IEEE citation format.

---
Make every section analytically rich. The report should demonstrate deep understanding of the experiment, not just describe what was done."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data:
        return Response("Invalid request", status=400)

    prompt = build_prompt(data)

    def stream():
        try:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            ) as stream_obj:
                for text in stream_obj.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    content = data.get("content", "")
    title = data.get("title", "lab_report")
    filename = title.strip().replace(" ", "_").lower() + "_report.md"

    return Response(
        content,
        mimetype="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
