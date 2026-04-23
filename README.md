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


## Persistence Justification as requied in the document (Requirement number 3)
I chose **SQLite** for persistence because it provides a lightweight, serverless relational structure that ensures data integrity across conversation turns. It allows for complex keyword and tag-based queries that would be inefficient in a plain JSON file.

##  Tool Schema Documentation as required (Requirement number 5)

| Tool           | Parameters                            | Return Type | Description 

| `Notes`        | `title`, `content`, `tags`            | `str`       | Creates a new note record in the SQLite DB. 
| `search_notes` | `query`                               |`list[dict]` | Searches titles, content, and tags using keyword matching.
| `update_note`  | `note_id`, `new_content`, `new_title` | `str`       | Updates specific fields of an existing note by ID.
| `delete_note`  | `note_id`                             | `str`       | Permanently removes a note from the database.

##  Evaluation Harness (Requirement 2.2)
The `evaluate_agent.py` script runs a suite of 12 test cases covering:
- **Happy Paths:** Note creation, keyword search, and summarization.
- **Intent Disambiguation:** Handling vague queries.
- **Edge Cases:** Graceful handling of "not found" results.
- **Safety:** Triggering human-in-the-loop interrupts for deletions.