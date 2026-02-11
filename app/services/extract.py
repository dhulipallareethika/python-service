import json
import re
from app.services.prompts import getPromptExtractStructure
from app.kadalClient import get_chat_completion # Ensure this import matches your client name

async def extract_project_structure(text: str, project_id: str) -> dict:
    messages = getPromptExtractStructure(text, project_id)
    raw_response = await get_chat_completion(messages)
    clean_json = re.sub(r'```json|```', '', raw_response).strip()
    
    try:
        structured_data = json.loads(clean_json)
        return structured_data
    except json.JSONDecodeError:
        return {
            "project_id": project_id,
            "classes": [],
            "error": "Failed to parse AI response into JSON"
        }