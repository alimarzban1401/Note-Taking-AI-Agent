from typing import List, Optional
from langchain_core.tools import tool
from database import DatabaseManager

# Anchor: Connection to our SQLite filing cabinet
db = DatabaseManager()

@tool
def create_note(title: str, content: str, tags: List[str]) -> str:
    """
    Creates a new note. 
    Use this when the user wants to save or record information.
    """
    # Memory: Returns ID so the agent can confirm success specifically
    note_id = db.add_note(title, content, tags)
    return f"Successfully created note with ID: {note_id}"

@tool
def search_notes(query: Optional[str] = None, tag: Optional[str] = None) -> str:
    """
    Searches notes by keyword or tag. 
    Use this for 'What did I write...' or 'Find my notes...'.
    """
    results = db.search_notes(query=query, tag=tag)
    
    # Memory: Handle the 'Empty' state gracefully for the LLM
    if not results:
        return "No notes found matching those criteria."
    
    # Memory: Convert list of dictionaries into a clean string for Claude to read
    output = []
    for r in results:
        output.append(f"ID: {r['id']} | Title: {r['title']}\nContent: {r['content']}\nTags: {r['tags']}\n---")
    
    return "\n".join(output)

@tool
def update_note(note_id: int, title: Optional[str] = None, content: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    Modifies an existing note by its ID. 
    Use this when the user wants to edit or change a note.
    """
    # Memory: Returns a boolean success to let the agent know if the ID existed
    success = db.update_note(note_id, title, content, tags)
    if success:
        return f"Note {note_id} updated successfully."
    return f"Error: Note ID {note_id} not found."

@tool
def delete_note(note_id: int) -> str:
    """
    Deletes a note permanently. 
    IMPORTANT: Destructive action.
    """
    # Memory: Simple ID-based deletion
    success = db.delete_note(note_id)
    if success:
        return f"Note {note_id} deleted successfully."
    return f"Error: Could not delete. Note ID {note_id} does not exist."