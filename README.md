# 🚀 Prospecting Tool — Setup Guide

## What this does
Generates personalised LinkedIn + email outreach sequences using AI,
then pushes leads directly into your Lemlist campaign.

---

## Setup (one time only)

### 1. Make sure Python is installed
Open Terminal and type:
```
python3 --version
```
If you see a version number, you're good. If not, download from python.org

### 2. Install the required packages
In Terminal, navigate to this folder and run:
```
pip3 install -r requirements.txt
```

### 3. Run the tool
```
python3 app.py
```

### 4. Open in your browser
Go to: http://localhost:5050

---

## Every time you use it
Just run:
```
python3 app.py
```
Then open http://localhost:5050

---

## Settings tab — what you need
- **Anthropic API key**: get from console.anthropic.com → API Keys
- **Lemlist API key**: Lemlist → Settings → Integrations → Generate key
- **Campaign ID**: open your campaign in Lemlist, copy the `cam_...` part from the URL

---

## How to use
1. Settings tab → enter your API keys
2. Prospect tab → fill in prospect details + your value prop
3. Hit Generate → review the 5-step sequence
4. Hit Push to Lemlist → lead is added to your campaign automatically
5. Lemlist handles all sending — you step in when they reply
