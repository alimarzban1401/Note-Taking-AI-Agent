# Note-Taking AI Agent

A stateful AI agent built with LangGraph and Anthropic's Claude Sonnet 4.6

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `.\venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure API: Rename `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`.

## Features
- **Persistence:** All notes are saved in a local SQLite database (`notes.db`).
- **Human-in-the-Loop:** Requires manual confirmation (y/n) before deleting or updating notes.
- **Context Awareness:** Remembers previous parts of the conversation.
- **Disambiguation:** Asks for clarification if a request is vague.

## How to Run
- Start the agent: `python agent.py`
- Run automated tests: `python evaluate_agent.py`