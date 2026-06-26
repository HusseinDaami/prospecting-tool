import os
import json
import base64
import anthropic
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    fname = data.get('fname', '')
    lname = data.get('lname', '')
    role = data.get('role', '')
    company = data.get('company', '')
    email = data.get('email', '')
    industry = data.get('industry', '')
    value_prop = data.get('value_prop', '')
    tone = data.get('tone', 'Direct & concise')
    anthropic_key = data.get('anthropic_key', '')

    if not anthropic_key:
        return jsonify({'error': 'Anthropic API key is required'}), 400

    full_name = f"{fname} {lname}".strip()

    prompt = f"""You are a B2B sales copywriter. Return ONLY a raw JSON array. No markdown, no backticks, no commentary. Just the JSON array starting with [ and ending with ].

Prospect: {full_name}{f', {role}' if role else ''}{f' at {company}' if company else ''}{f' ({industry})' if industry else ''}
Value proposition: {value_prop}
Tone: {tone}

Return exactly this structure:
[{{"step":1,"channel":"LinkedIn","type":"Connection request","day":"Day 1","subject":null,"body":"..."}},{{"step":2,"channel":"LinkedIn","type":"Follow-up message","day":"Day 3","subject":null,"body":"..."}},{{"step":3,"channel":"Email","type":"Cold email","day":"Day 5","subject":"...","body":"..."}},{{"step":4,"channel":"Email","type":"Follow-up email","day":"Day 8","subject":"...","body":"..."}},{{"step":5,"channel":"Email","type":"Final bump","day":"Day 12","subject":"...","body":"..."}}]

Rules:
- LinkedIn connection request: max 280 characters, no subject
- LinkedIn follow-up: 2-3 short sentences, warm, no subject
- Emails: short paragraphs, no buzzwords, soft CTA, sign off naturally
- Personalise using prospect name, role, company, industry
- Each step has a fresh angle"""

    try:
        client = anthropic.Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        if not raw.startswith('['):
            import re
            match = re.search(r'\[[\s\S]*\]', raw)
            if match:
                raw = match.group(0)
        steps = json.loads(raw)
        return jsonify({'steps': steps})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/push', methods=['POST'])
def push_to_lemlist():
    data = request.json
    lemlist_key = data.get('lemlist_key', '')
    campaign_id = data.get('campaign_id', '')
    email = data.get('email', '')

    if not lemlist_key:
        return jsonify({'error': 'Lemlist API key is required'}), 400
    if not campaign_id:
        return jsonify({'error': 'Campaign ID is required'}), 400
    if not email:
        return jsonify({'error': 'Prospect email is required'}), 400

    payload = {'email': email}
    if data.get('fname'): payload['firstName'] = data['fname']
    if data.get('lname'): payload['lastName'] = data['lname']
    if data.get('company'): payload['companyName'] = data['company']
    if data.get('role'): payload['jobTitle'] = data['role']
    if data.get('linkedin'): payload['linkedinUrl'] = data['linkedin']

    encoded = base64.b64encode(f':{lemlist_key}'.encode()).decode()
    try:
        res = requests.post(
            f'https://api.lemlist.com/api/campaigns/{campaign_id}/leads/',
            headers={'Authorization': f'Basic {encoded}', 'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        if res.ok:
            return jsonify({'success': True, 'message': f'{data.get("fname") or email} added to your Lemlist campaign!'})
        else:
            err = res.json()
            return jsonify({'error': err.get('message') or err.get('error') or f'Lemlist error {res.status_code}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


