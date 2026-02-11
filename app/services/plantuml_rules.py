ERD_SPECIFIC_RULES = """
1. Use 'skinparam linetype ortho' and 'hide circle'.
2. Use 'entity "Entity Name" as alias {' for table structures.
3. Define fields with data types: '* **primary_key** : TYPE', 'field_name : TYPE'.
4. Mention **foreign_key** if any establishment of a relationship between tables by referencing the primary key of another table.
4. Use a horizontal line '--' to separate the primary key from other fields.
5. Use Crow's Foot notation for relationships:
   - Zero or Many: }o--
   - One or Many: }|--
   - Exactly One: ||--
6. Example: Entity01 ||--o{ Entity02 : "describes"
"""
SEQUENCE_RULES = """
1. Use 'autonumber' at the start.
2. Define participants early: 'participant "Display Name" as Alias'.
3. Use quotes around participant names if they contain spaces.
4. Use 'activate' immediately after a call and 'deactivate' after the return '-->'.
5. Ensure every 'alt' or 'loop' block is strictly closed with 'end'.
"""
CLASS_RULES = """
1. Use 'class "Name" {' and define fields first, then methods.
2. Use visibility: - (private), # (protected), + (public).
3. Use standard arrows: <|-- (Inheritance), *-- (Composition), o-- (Aggregation).
"""
USE_CASE_RULES = """
1. Use 'left to right direction'.
2. Wrap use cases in 'package "System Name" { ... }'.
3. Define actors with 'actor :Actor Name: as Alias'.
4. Show relationships: Use (Actor) --> (UseCase).
5. Include/Extend: Use (UC1) ..> (UC2) : <<include>> or <<extend>>.
6. For each actor try to give atleast 4 use cases
"""
COMPONENT_RULES = """
1. Use 'skinparam componentStyle uml2'.
2. Define components: 'component [Name] as Alias'.
3. Use interfaces: 'interface "API" as Alias' or '() "Name"'.
4. Grouping: Use 'package' or 'node'. 
5. Connections: 'Alias1 --> Alias2' or 'Alias1 ..> Alias2'.
"""
DATABASE_CODE_RULES = """
Task: Convert the provided PlantUML ERD and Requirements into Database Schemas.
1. For sql Generate:
    - SQL DDL statements
    - Primary and foreign keys
    - Constraints
    - Indexes
    - Production-ready schema
3. For noSql Generate:
    - NoSQL collection schema
    - Indexes
    - Validation rules
    - Sample CRUD queries
4. Ensure data types match the ERD precisely.
Format the output as a clean for both sql and nosql db codes
"""
API_CONTRACT_RULES = """
Task: Convert the provided PlantUML Sequence and Requirements into API Contracts.
Generate the latest OpenAPI version contract.
Rules:
- Use YAML
- Start the YAML with 'openapi: 3.1.0'
- Follow latest OpenAPI version specification strictly
- Include info, servers, paths, components
- Use versioned base path (/api/v1)
- Define request and response schemas clearly
- Include proper HTTP status codes
- Use bearer JWT authentication
- Include error responses (400, 401, 500)
- Use enums where applicable
- Follow industry best practices
Format the output as a clean YAML kind of output
"""