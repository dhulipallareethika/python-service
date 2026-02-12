from fastapi import FastAPI, Request, Body
from app.model import *
from app.services.generate import generate_diagram, generate_derived_artifact
from app.handlers import global_exception_handler, global_response_middleware
from fastapi.exceptions import RequestValidationError
from app.services.extract import extract_project_structure

app = FastAPI(title="Archie AI Service", openapi_version="3.0.2")
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

@app.middleware("http")
async def wrap_response(request: Request, call_next):
    """
    Standardizes the API response format globally.
    """
    return await global_response_middleware(request, call_next)

@app.post("/generate")
async def generate(request: GenerateRequest = Body(...)):
    diagramType = request.diagramType
    umlType = request.umlType
    if diagramType == DiagramType.DATABASE:
        uml_context = await generate_diagram(
            "ERD",
            request.requirementsText,
            "PLANTUML",
            request.classes,
            flag=True
        )
        final_output = await generate_derived_artifact(
            "DATABASE",
            request.requirementsText,
            uml_context,
            request.classes
        )
        return {
            "diagramType": diagramType,
            "diagramLanguage": "SQL/NoSQL",
            "diagramCode": final_output,
            "isRenderable": False
        }
    if diagramType == DiagramType.API:
        final_output = await generate_derived_artifact(
            "API",
            request.requirementsText,
            "",  
            request.classes
        )
        return {
            "diagramType": diagramType,
            "diagramLanguage": "OPENAPI",
            "diagramCode": final_output,
            "isRenderable": False
        }
    diagram_code = await generate_diagram(
        diagramType.value,
        request.requirementsText,
        umlType,
        request.classes,
        flag=False
    )
    return {
        "diagramType": diagramType,
        "umlType": umlType,
        "diagramCode": diagram_code,
        "isRenderable": True
    }

@app.post("/extract", response_model=ProjectResponse)
async def extract_structure(request: ExtractionRequest = Body(...)):
    """
    Analyzes raw text requirements and extracts the structured JSON classes 
    required for the /generate endpoint.
    """
    structured_data = await extract_project_structure(
        request.requirementsText, 
        request.projectName
    )
    return structured_data
