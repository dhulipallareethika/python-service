from pydantic import BaseModel, field_validator
from typing import Optional, Any,List
from enum import Enum

class DiagramType(str, Enum):
    DATABASE = "DATABASE"
    API = "API"
    ERD = "ERD"
    SEQUENCE = "SEQUENCE"
    CLASS = "CLASS"
    USE_CASE = "USE_CASE"
    COMPONENT = "COMPONENT"

class DiagramBaseModel(BaseModel):
    diagramType: DiagramType
    
    @field_validator("diagramType", mode="before")
    @classmethod
    def normalize_diagram_type(cls, v):
        if isinstance(v, str):
            return v.upper().replace(" ", "_")
        return v

class RefineRequest(DiagramBaseModel):
    existingDiagramCode: str
    userInstruction: str
    umlType:str

class AttributeNature(str, Enum):
    Identifying = "Identifying"
    Descriptive = "Descriptive"
    Optional = "Optional"

class RelationshipNature(str, Enum):
    Association = "Association"
    Aggregation = "Aggregation"
    Composition = "Composition"

class RelationshipType(str, Enum):
    One = "One"
    Many = "Many"

class Attribute(BaseModel):
    name: str
    type: str
    nature: AttributeNature
    required: bool

class Relationship(BaseModel):
    source: str
    target: str
    nature: RelationshipNature
    sourcetype: RelationshipType
    targettype: RelationshipType
    label: Optional[str] = None

class ClassModel(BaseModel):
    className: str
    attributes: List[Attribute]
    relationships: List[Relationship]

class ProjectResponse(BaseModel):
    projectName: str
    classes: List[ClassModel]

class ExtractionRequest(BaseModel):
    projectName: str
    requirementsText: str
class ErrorResponse(BaseModel):
    message: str
    code: str

class ApiResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    error: Optional[ErrorResponse] = None

class GenerateRequest(DiagramBaseModel):
    requirementsText: str
    umlType: str
    classes: List[ClassModel]