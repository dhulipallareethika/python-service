from fastapi import FastAPI, Request
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
    return await global_response_middleware(request, call_next)

@app.post("/generate")
async def generate(request: GenerateRequest):
    diagramType = request.diagramType
    diagramLanguage=request.diagramLanguage
    
    if diagramType in [DiagramType.DATABASE, DiagramType.API]:
        is_db = (diagramType == DiagramType.DATABASE)
        base_type = "ERD" if is_db else "Sequence Diagram"
        
        uml_context = await generate_diagram(base_type, request.requirementsText,"PLANTUML")
        final_output = await generate_derived_artifact(diagramType.value, request.requirementsText, uml_context)
        return {
            "diagramType": diagramType,
            "diagramLanguage": "JSON/SQL" if is_db else "OPENAPI",
            "diagramCode": final_output,
            "isRenderable": False
        }
    
    diagram_code = await generate_diagram(diagramType.value, request.requirementsText,request.diagramLanguage)
    return {
        "diagramType": diagramType,
        "diagramLanguage":diagramLanguage,
        "diagramCode": diagram_code,
        "isRenderable": True
    }


@app.post("/extract", response_model=ProjectResponse)
async def extract_structure(request: ExtractionRequest):
    """
    Takes requirementsText from backend and returns structured ProjectResponse.
    """
    structured_data = await extract_project_structure(
        request.requirementsText, 
        request.project_id
    )
    return structured_data