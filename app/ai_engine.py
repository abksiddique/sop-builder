import re
import json
import requests
from flask import current_app


def call_gemini(prompt):
    try:
        api_key = current_app.config.get('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4000}
        }
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'], 'gemini-1.5-flash'
    except Exception as e:
        print(f"Gemini failed: {e}")
        return None, None


def call_groq(prompt):
    try:
        api_key = current_app.config.get('GROQ_API_KEY')
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.3
        }
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'], 'groq-llama-3.3-70b'
    except Exception as e:
        print(f"Groq failed: {e}")
        return None, None


def generate_text(prompt):
    result, model = call_gemini(prompt)
    if result:
        return result, model
    print("Gemini unavailable. Falling back to Groq...")
    result, model = call_groq(prompt)
    if result:
        return result, model
    return None, None


def build_sop_prompt(process_name, description, roles, exceptions):
    return f"""
You are an expert technical writer specializing in Standard Operating Procedures (SOPs).

Generate a complete, professional SOP document for the following process.
Use EXACTLY this structure with these exact headings:

# {process_name}

## 1. Purpose
[Why this process exists and what problem it solves]

## 2. Scope
[Who this SOP applies to and what it covers]

## 3. Roles and Responsibilities
[List each role and their specific responsibilities in this process]

## 4. Prerequisites
[What must be in place before starting this process]

## 5. Procedure
[Numbered step-by-step instructions. Be specific and clear.
Include decision points where relevant.]

## 6. Exceptions and Edge Cases
[How to handle deviations, errors, and unusual situations]

## 7. Governance
[Who owns this SOP, review frequency, and what triggers an update]

## 8. Improvement Recommendation
[At least one concrete suggestion to improve this process with rationale]

---

PROCESS DETAILS:
- Process Name: {process_name}
- Description: {description}
- Roles Involved: {roles if roles else 'Not specified'}
- Known Exceptions: {exceptions if exceptions else 'Not specified'}

Write in clear, professional language. Be specific and actionable.
Do not add any text before or after the SOP document itself.
"""


def build_bpmn_prompt(process_name, description, roles, exceptions):
    return f"""
You are a BPMN 2.0 expert. Generate valid BPMN 2.0 XML for the following process.

STRICT REQUIREMENTS:
1. Return ONLY raw XML. No explanations, no markdown, no code blocks.
2. Start with: <?xml version="1.0" encoding="UTF-8"?>
3. Use this exact namespace: xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
4. Include: start event, tasks for each main step, at least one gateway for decisions, end event.
5. Include BPMNDiagram section with BPMNShape bounds so bpmn-js can render it.
6. If exceptions exist, include an exception path.

PROCESS DETAILS:
- Process Name: {process_name}
- Description: {description}
- Roles: {roles if roles else 'Single actor'}
- Exceptions: {exceptions if exceptions else 'None specified'}

Return only valid BPMN 2.0 XML. Nothing else.
"""


def build_diagram_json_prompt(process_name, description, roles, exceptions):
    return f"""
You are a process analyst. Extract the main steps from this process and return ONLY a valid JSON object.

Return exactly this structure:
{{
  "steps": [
    {{"id": "A", "type": "start", "label": "Start"}},
    {{"id": "B", "type": "task", "label": "First Step Name"}},
    {{"id": "C", "type": "decision", "label": "Condition Met"}},
    {{"id": "D", "type": "task", "label": "Handle Yes Case"}},
    {{"id": "E", "type": "task", "label": "Handle No Case"}},
    {{"id": "Z", "type": "end", "label": "End"}}
  ],
  "connections": [
    {{"from": "A", "to": "B"}},
    {{"from": "B", "to": "C"}},
    {{"from": "C", "to": "D", "label": "Yes"}},
    {{"from": "C", "to": "E", "label": "No"}},
    {{"from": "D", "to": "Z"}},
    {{"from": "E", "to": "Z"}}
  ]
}}

STRICT RULES:
- Maximum 12 steps
- step type must be one of: start, task, decision, end
- Labels: max 5 words, letters and spaces only, no special characters
- Decision labels should be a short question without question mark
- Every connection must reference a valid step id
- There must be exactly one start and one end
- Return ONLY the JSON object. No explanation. No markdown. No code fences.

PROCESS TO DIAGRAM:
- Name: {process_name}
- Description: {description}
- Roles: {roles if roles else 'Not specified'}
- Exceptions: {exceptions if exceptions else 'None'}
"""


def json_to_mermaid(raw):
    try:
        # Clean markdown fences if present
        clean = raw.strip()
        clean = re.sub(r'^```[a-zA-Z]*\n?', '', clean)
        clean = re.sub(r'\n?```$', '', clean)
        clean = clean.strip()

        data = json.loads(clean)
        steps = data.get('steps', [])
        connections = data.get('connections', [])

        if not steps or not connections:
            print("JSON diagram: empty steps or connections")
            return None

        lines = ['flowchart TD']

        # Build node definitions
        for step in steps:
            sid = str(step.get('id', 'X'))
            label = str(step.get('label', 'Step')).strip()
            # Remove any characters that could break Mermaid
            label = re.sub(r'["\{\}\[\]\(\)]', '', label)
            stype = step.get('type', 'task')

            if stype in ('start', 'end'):
                lines.append('    ' + sid + '((' + label + '))')
            elif stype == 'decision':
                lines.append('    ' + sid + '{' + label + '?}')
            else:
                lines.append('    ' + sid + '[' + label + ']')

        lines.append('')

        # Build connections
        for conn in connections:
            frm = str(conn.get('from', ''))
            to = str(conn.get('to', ''))
            lbl = str(conn.get('label', '')).strip()
            lbl = re.sub(r'["\{\}\[\]]', '', lbl)

            if frm and to:
                if lbl:
                    lines.append('    ' + frm + ' -->|' + lbl + '| ' + to)
                else:
                    lines.append('    ' + frm + ' --> ' + to)

        mermaid = '\n'.join(lines)
        print(f"--- GENERATED MERMAID ---\n{mermaid}\n--- END ---")
        return mermaid

    except Exception as e:
        print(f"json_to_mermaid failed: {e}")
        print(f"Raw input was: {raw}")
        return None


def clean_code_block(text):
    if not text:
        return text
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```[a-z]*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()
    return text


def generate_sop(process_name, description, roles, exceptions):
    # Step 1 — Generate SOP text
    sop_prompt = build_sop_prompt(process_name, description, roles, exceptions)
    sop_content, model_used = generate_text(sop_prompt)

    if not sop_content:
        return None, None, None, "Both AI services failed. Please try again."

    # Step 2 — Generate BPMN XML for download
    bpmn_prompt = build_bpmn_prompt(process_name, description, roles, exceptions)
    bpmn_xml, _ = generate_text(bpmn_prompt)
    bpmn_xml = clean_code_block(bpmn_xml)

    # Step 3 — Ask LLM for JSON steps, convert to Mermaid in Python
    diagram_prompt = build_diagram_json_prompt(process_name, description, roles, exceptions)
    diagram_json, _ = generate_text(diagram_prompt)
    mermaid_code = None

    if diagram_json:
        mermaid_code = json_to_mermaid(diagram_json)

    return sop_content, bpmn_xml, mermaid_code, model_used