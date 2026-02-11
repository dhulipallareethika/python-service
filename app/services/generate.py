import re,json
from app.kadalClient import get_chat_completion
from app.services.plantuml_rules import (ERD_SPECIFIC_RULES, SEQUENCE_RULES, CLASS_RULES, COMPONENT_RULES, DATABASE_CODE_RULES, API_CONTRACT_RULES, USE_CASE_RULES)
from app.services.prompts import getPromptMessage, getPromptDerivedArtifact

async def generate_derived_artifact(artifact_type: str, requirements: str, source_uml: str) -> str:
    diag_type_key = artifact_type.upper()
    if "DATABASE" in diag_type_key:
        extra_context = DATABASE_CODE_RULES
    else:
        extra_context = API_CONTRACT_RULES
    messages = getPromptDerivedArtifact(extra_context, source_uml, requirements)
    llm_response = await get_chat_completion(messages)
    return llm_response
def clean_plantuml_code(raw_code: str) -> str:
    if not raw_code: return ""
    cleaned = re.sub(r'```(?:plantuml|puml|text)?', '', raw_code)
    cleaned = cleaned.replace('```', '').strip()
    return cleaned
async def generate_diagram(diagram_type: str, requirements: str,language:str) -> str:
    diag_type_key = diagram_type.upper()
    language_key=language.upper()
    is_json_input = False
    try:
        json_data = json.loads(requirements)
        is_json_input = True
        
        # Extract the actual data if it's wrapped in your "SUCCESS" format
        if "data" in json_data and "classes" in json_data["data"]:
            actual_schema = json_data["data"]
        elif "classes" in json_data:
            actual_schema = json_data
        else:
            actual_schema = json_data
            
        requirements = (
            f"ACT AS A TRANSLATOR. Convert this JSON SCHEMA into a {diag_type_key} diagram. "
            f"Schema: {json.dumps(actual_schema)}"
        )
    except (ValueError, TypeError):
        is_json_input = False
    MAPPING = {
        "PLANTUML": {
            ("ERD", "ENTITY RELATIONSHIP"): ERD_SPECIFIC_RULES,
            ("SEQUENCE",): SEQUENCE_RULES,
            ("CLASS",): CLASS_RULES,
            ("USE CASE", "USE_CASE"): USE_CASE_RULES,
            ("COMPONENT",): COMPONENT_RULES,
        }}
    selected_language_rules = MAPPING.get(language_key, MAPPING["PLANTUML"])
    extra_context = "Generate a standard, clean {language_key} diagram."
    for keywords, context in selected_language_rules.items():
        if any(key in diag_type_key for key in keywords):
            extra_context = context
            break
    if is_json_input:
        extra_context = (
            f"STRICT SCHEMA MAPPING: Transform the provided JSON into a {diag_type_key}. "
            "Do not invent new entities unless necessary for diagram validity. "
            f"Follow these specific rules: {extra_context}"
        )
    messages = getPromptMessage(diagram_type, extra_context, requirements,language)
    raw_response = await get_chat_completion(messages)
    actual_response = clean_plantuml_code(raw_response) 
    print(actual_response)
    return actual_response