# Monday.com BI Agent

An AI-powered Business Intelligence agent that fetches real-time data from monday.com boards (Deals & Work Orders) and provides executive insights.

**For Evaluation:** [Decision Log](DECISION_LOG.md) | [Submission ZIP](Skylark_BI_Agent_Submission.zip)

**Live Demo:** [https://monday-bi-agent-beta.vercel.app/](https://monday-bi-agent-beta.vercel.app/)  
**Source Code:** [https://github.com/NilinR/Monday.com_BI_Agent](https://github.com/NilinR/Monday.com_BI_Agent)

## Overview
This full-stack application utilizes a FastAPI Python backend and a React (Vite) frontend to ingest, sanitize, and analyze live CRM data. It uses the Gemini 3.1 Flash-Lite LLM to provide on-demand executive insights and risk analysis.

## Setup & Local Run

### Prerequisites
* Python 3.10+
* Node.js & npm
* Monday.com API Token
* Gemini API Key

### 1. Backend Setup
Navigate to the root directory and install the required Python packages:
```bash
pip install -r requirements.txt