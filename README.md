\# AI App Builder



An AI-powered application development tool that helps users transform an application idea into a structured development process through:



Prompt → Understand → Plan → Build → Explain → Learn



The goal of this project is to go beyond simple AI code generation. Instead of only generating an application from a prompt, the tool uses AI throughout the application development lifecycle to help users understand requirements, design the solution, generate the application, understand the generated code, and learn the technologies and concepts involved.



\---



\## Overview



AI App Builder is a web-based prototype designed to demonstrate how generative AI can assist developers throughout the software development process.



A user provides an application idea such as:



"I want to build a personal expense tracker where users can add expenses, categorize them, view monthly spending, and see summaries."



The system then guides the user through five AI-assisted stages:



1\. Understand — analyzes and structures the application requirements.

2\. Plan — creates a technical architecture and development plan.

3\. Build — generates a runnable MVP project with multiple source files.

4\. Explain — explains the generated application, architecture, files, and data flow.

5\. Learn — creates a learning guide based on the technologies and concepts involved.



The application also provides user authentication and persistent project storage.



\---



\## Key Features



\### 1. AI Requirement Understanding



The user provides a natural-language application idea.



The AI analyzes the request and identifies important requirements such as:



\- Application purpose

\- Target users

\- Core features

\- Functional requirements

\- Non-functional requirements

\- Inputs and outputs

\- Main entities

\- Expected application behavior



\### 2. AI-Powered Technical Planning



The system converts the application understanding into a practical technical plan.



The generated plan can include:



\- Architecture

\- Technology stack

\- Database design

\- Application components

\- API design

\- Development phases

\- Security considerations

\- Deployment plan



The planning stage is designed to keep the generated architecture realistic for an MVP instead of unnecessarily introducing complex technologies.



\### 3. AI Application Builder



The Build stage converts the application requirements and technical plan into an application structure.



The AI first determines the minimum set of required files and then generates each file individually.



The generated result includes:



\- Project name

\- Project description

\- Technology stack

\- Project structure

\- Source files

\- File purposes

\- Run instructions



The prototype supports multi-file application generation while keeping the generated project relatively small and understandable.



\### 4. AI Code and Architecture Explanation



The Explain stage helps developers understand the generated application.



It provides:



\- Application overview

\- Architecture explanation

\- Technology explanations

\- File-by-file explanations

\- Application flow

\- Important concepts

\- Data flow

\- Key takeaways



This makes the tool useful not only for generating applications but also for understanding how the generated application works.



\### 5. AI Learning Guide



The Learn stage transforms the generated application into a personalized learning guide.



It provides:



\- Learning overview

\- Technologies to learn

\- Core concepts

\- Learning path

\- Practice tasks

\- Suggested improvements

\- Challenge questions

\- Skills gained



This allows users to learn the concepts behind the application rather than treating AI-generated code as a black box.



\---



\## AI-Assisted Development Workflow



&#x20;   USER PROMPT

&#x20;        |

&#x20;        v

&#x20;   +-------------------+

&#x20;   |    UNDERSTAND     |

&#x20;   | Requirements      |

&#x20;   | Analysis          |

&#x20;   +---------+---------+

&#x20;             |

&#x20;             v

&#x20;   +-------------------+

&#x20;   |       PLAN        |

&#x20;   | Architecture      |

&#x20;   | Technology Stack  |

&#x20;   | Database / APIs   |

&#x20;   +---------+---------+

&#x20;             |

&#x20;             v

&#x20;   +-------------------+

&#x20;   |       BUILD       |

&#x20;   | Project Structure |

&#x20;   | Source Files      |

&#x20;   | Run Instructions  |

&#x20;   +---------+---------+

&#x20;             |

&#x20;             v

&#x20;   +-------------------+

&#x20;   |      EXPLAIN      |

&#x20;   | Architecture      |

&#x20;   | Files             |

&#x20;   | Data Flow         |

&#x20;   +---------+---------+

&#x20;             |

&#x20;             v

&#x20;   +-------------------+

&#x20;   |       LEARN       |

&#x20;   | Concepts          |

&#x20;   | Learning Path     |

&#x20;   | Practice Tasks    |

&#x20;   +-------------------+



\---



\## System Architecture



&#x20;   Internet

&#x20;      |

&#x20;      v

&#x20;   +---------------------------+

&#x20;   |    Streamlit Frontend     |

&#x20;   |    Streamlit Community    |

&#x20;   |    Cloud                  |

&#x20;   +-------------+-------------+

&#x20;                 |

&#x20;                 | HTTP API

&#x20;                 v

&#x20;   +---------------------------+

&#x20;   |      FastAPI Backend      |

&#x20;   |          Render           |

&#x20;   +-------------+-------------+

&#x20;                 |

&#x20;                 v

&#x20;   +---------------------------+

&#x20;   |    Hugging Face Inference |

&#x20;   |          API              |

&#x20;   |  Qwen3-4B-Instruct-2507   |

&#x20;   +---------------------------+



&#x20;                 |

&#x20;         +-------+-------+

&#x20;         |               |

&#x20;         v               v

&#x20;   +-------------+   +----------------+

&#x20;   |  Supabase   |   | Generated App  |

&#x20;   |             |   |    Content     |

&#x20;   | Auth        |   |                |

&#x20;   | PostgreSQL  |   |                |

&#x20;   | RLS         |   |                |

&#x20;   +-------------+   +----------------+



\---



\## Technology Stack



\### Frontend



\- Python

\- Streamlit



\### Backend



\- Python

\- FastAPI

\- Uvicorn

\- Pydantic



\### AI



\- Hugging Face Inference API

\- Qwen3-4B-Instruct-2507

\- Structured JSON generation

\- Prompt-based AI workflows



\### Database



\- Supabase

\- PostgreSQL



\### Authentication



\- Supabase Auth

\- Email authentication



\### Security



\- Supabase Row Level Security (RLS)

\- Environment-based secrets

\- Streamlit Secrets Management



\### Deployment



\- GitHub

\- Streamlit Community Cloud

\- Render



\---



\## AI Technologies Used



\### Qwen3-4B-Instruct-2507



The application uses the Qwen3-4B-Instruct-2507 model through the Hugging Face Inference API.



The model is used for:



\- Requirement analysis

\- Technical planning

\- Application file generation

\- Code and architecture explanation

\- Learning guide generation



\### Hugging Face Inference API



The Hugging Face Inference API provides access to the generative AI model from the FastAPI backend.



The backend sends structured prompts containing the application requirements and receives AI-generated responses.



\### Structured AI Generation



The system instructs the AI to return structured JSON for stages where predictable application data is required.



For example, the planning stage returns structured information for:



\- Architecture

\- Technology Stack

\- Database Design

\- Application Components

\- API Design

\- Development Phases

\- Security Considerations

\- Deployment Plan



A shared JSON parsing utility handles valid JSON, fenced JSON responses, and recoverable JSON embedded inside model responses.



\---



\## Backend API



The FastAPI backend exposes the following endpoints.



\### Health Check



GET /api/health



Used to verify that the backend service is running.



\### Understand



POST /api/understand



Analyzes the user's application requirements.



\### Plan



POST /api/plan



Creates a technical development plan based on the application requirements.



\### Build



POST /api/build



Generates the application structure and source files.



The Build workflow:



&#x20;   Application Request

&#x20;           |

&#x20;           v

&#x20;   Generate File Manifest

&#x20;           |

&#x20;           v

&#x20;   Generate Individual Files

&#x20;           |

&#x20;           v

&#x20;   Assemble Project

&#x20;           |

&#x20;           v

&#x20;   Return Generated Application



\### Explain



POST /api/explain



Explains the generated application and its architecture.



\### Learn



POST /api/learn



Creates a learning guide based on the generated application.



\---



\## Project Structure



&#x20;   ai-app-builder/

&#x20;   |

&#x20;   +-- api/

&#x20;   |   +-- \_\_init\_\_.py

&#x20;   |   +-- main.py

&#x20;   |   +-- routes.py

&#x20;   |   +-- schemas.py

&#x20;   |

&#x20;   +-- core/

&#x20;   |   +-- \_\_init\_\_.py

&#x20;   |   +-- api\_client.py

&#x20;   |   +-- json\_utils.py

&#x20;   |   +-- llm.py

&#x20;   |   +-- project\_service.py

&#x20;   |   +-- supabase\_client.py

&#x20;   |

&#x20;   +-- pages/

&#x20;   |   +-- login.py

&#x20;   |   +-- dashboard.py

&#x20;   |   +-- workspace.py

&#x20;   |

&#x20;   +-- app.py

&#x20;   +-- requirements.txt

&#x20;   +-- .gitignore

&#x20;   +-- README.md



\---



\## Application Components



\### app.py



Main Streamlit application entry point.



It controls the application entry flow and navigation.



\### pages/login.py



Handles:



\- User login

\- User registration

\- Authentication state

\- Logout functionality



\### pages/dashboard.py



Provides:



\- Application creation

\- User's application list

\- Project selection

\- Workspace navigation



\### pages/workspace.py



Provides the main AI App Builder workspace.



The workspace contains the five development stages:



\- Understand

\- Plan

\- Build

\- Explain

\- Learn



\### core/llm.py



Provides the interface to the Hugging Face Inference API and Qwen3 model.



\### core/api\_client.py



Provides communication between the Streamlit frontend and FastAPI backend.



The API URL can be configured through the deployment environment or Streamlit Secrets.



\### core/json\_utils.py



Provides shared parsing logic for AI-generated JSON responses.



\### core/project\_service.py



Handles project operations with Supabase, including:



\- Creating projects

\- Retrieving user projects

\- Updating project sections



\### core/supabase\_client.py



Provides the Supabase client used by the Streamlit application.



\### api/main.py



Creates and configures the FastAPI application.



\### api/routes.py



Contains the AI workflow API endpoints:



\- /api/health

\- /api/understand

\- /api/plan

\- /api/build

\- /api/explain

\- /api/learn



\### api/schemas.py



Defines Pydantic request and response models used by the FastAPI backend.



\---



\## Database Design



The application uses Supabase PostgreSQL.



The main table is:



&#x20;   projects



The project records contain information such as:



\- id

\- user\_id

\- name

\- prompt

\- understanding

\- plan

\- generated\_code

\- explanation

\- learning\_content

\- created\_at

\- updated\_at



The AI-generated workflow results are stored as structured JSON data.



This allows users to return to previously created applications without regenerating all AI results.



\---



\## Authentication and Security



The application uses Supabase Authentication for user accounts.



Each project is associated with the authenticated user's ID.



Row Level Security (RLS) is enabled on the projects table.



Users can:



\- View their own projects

\- Create their own projects

\- Update their own projects

\- Delete their own projects



Users cannot access another user's project records through the application.



Sensitive configuration values such as:



\- Supabase credentials

\- Hugging Face API token

\- Production API URL



are kept outside the source code using secrets and environment configuration.



The Hugging Face token is never stored in the GitHub repository.



\---



\## Deployment Architecture



The prototype is deployed using separate frontend and backend services.



\### Frontend



Streamlit Community Cloud



The Streamlit application provides the user interface.



\### Backend



Render



The FastAPI backend handles AI requests.



\### AI



Hugging Face Inference API



&#x20;   Hugging Face Inference API

&#x20;             |

&#x20;             v

&#x20;   Qwen3-4B-Instruct-2507



\### Database and Authentication



Supabase



This separation keeps the Streamlit interface and FastAPI AI backend independently deployable.



\---



\## Environment Configuration



The application requires the following configuration values.



\### Streamlit Secrets



\- SUPABASE\_URL

\- SUPABASE\_KEY

\- HF\_TOKEN

\- API\_BASE\_URL



API\_BASE\_URL points the Streamlit frontend to the deployed FastAPI backend.



Example:



&#x20;   API\_BASE\_URL=https://your-fastapi-service.onrender.com



Actual credentials and tokens should never be committed to GitHub.



\---



\## Local Development



\### 1. Clone the repository



&#x20;   git clone https://github.com/YOUR\_USERNAME/ai-app-builder.git

&#x20;   cd ai-app-builder



\### 2. Create a virtual environment



&#x20;   python -m venv .venv



\### 3. Activate the virtual environment



Windows PowerShell:



&#x20;   .\\.venv\\Scripts\\Activate.ps1



\### 4. Install dependencies



&#x20;   pip install -r requirements.txt



\### 5. Configure secrets



Create:



&#x20;   .streamlit/secrets.toml



with the required Supabase and Hugging Face configuration.



Do not commit this file to GitHub.



\### 6. Start FastAPI



Windows PowerShell:



&#x20;   $env:HF\_TOKEN="YOUR\_HUGGING\_FACE\_TOKEN"

&#x20;   python -m uvicorn api.main:app --reload --port 8000



\### 7. Start Streamlit



In another PowerShell terminal:



&#x20;   streamlit run app.py



The frontend will normally be available at:



&#x20;   http://localhost:8501



The FastAPI backend will normally be available at:



&#x20;   http://127.0.0.1:8000



\---



\## Example Application Workflow



A user can enter:



&#x20;   I want to build a personal expense tracker where users can

&#x20;   add expenses, categorize them, view monthly spending, and

&#x20;   see summaries.



The system then processes the request:



&#x20;   User Idea

&#x20;      |

&#x20;      v

&#x20;   Understand

&#x20;      |

&#x20;      v

&#x20;   Requirements

&#x20;      |

&#x20;      v

&#x20;   Plan

&#x20;      |

&#x20;      v

&#x20;   Architecture + Technology Stack

&#x20;      |

&#x20;      v

&#x20;   Build

&#x20;      |

&#x20;      v

&#x20;   Generated Project Files

&#x20;      |

&#x20;      v

&#x20;   Explain

&#x20;      |

&#x20;      v

&#x20;   Architecture + Code Understanding

&#x20;      |

&#x20;      v

&#x20;   Learn

&#x20;      |

&#x20;      v

&#x20;   Learning Path + Practice Tasks



\---



\## Design Principles



The prototype follows several principles.



\### Keep generated applications practical



The AI is instructed to avoid unnecessary technologies and focus on realistic MVP architectures.



\### Explain generated applications



Code generation alone is not enough. The system provides explanations of the generated project.



\### Promote learning



The Learn stage helps users understand the technologies and concepts behind their generated application.



\### Avoid unnecessary complexity



The prototype intentionally avoids introducing technologies that are not required by the application.



\### Separate frontend and backend responsibilities



Streamlit handles the user interface while FastAPI handles AI-related backend operations.



\---



\## Limitations



This is a working prototype rather than a production-scale application generation platform.



Current limitations include:



\- Generated applications are MVP-oriented.

\- Generated code is not automatically deployed as an independent application.

\- AI-generated code should be reviewed and tested before production use.

\- The prototype does not execute generated code in an isolated sandbox.

\- Large applications may require additional architecture and validation.

\- AI-generated responses depend on the capabilities and limitations of the selected language model.



\---



\## Future Improvements



Potential future enhancements include:



\- Automatic generated application deployment

\- Code execution in a secure sandbox

\- Project file download as ZIP

\- GitHub repository generation

\- AI-powered code validation

\- Automated testing of generated applications

\- Iterative code modification through natural-language instructions

\- Version history for generated applications

\- AI debugging assistance

\- Application preview

\- Support for additional AI models

\- Streaming AI responses

\- More advanced project planning and dependency analysis



\---



\## What Makes This Project Different



Traditional AI application generators often focus mainly on:



&#x20;   Prompt → Generate Code



This project explores a broader development experience:



&#x20;   Prompt

&#x20;      |

&#x20;      v

&#x20;   Understand

&#x20;      |

&#x20;      v

&#x20;   Plan

&#x20;      |

&#x20;      v

&#x20;   Build

&#x20;      |

&#x20;      v

&#x20;   Explain

&#x20;      |

&#x20;      v

&#x20;   Learn



The objective is to demonstrate how generative AI can support developers not only in writing code, but also in:



\- Understanding requirements

\- Designing software

\- Building applications

\- Understanding generated code

\- Learning software engineering concepts



\---



\## Project Status



The prototype is fully functional and deployed.



\### Current Status



\- \[x] User authentication

\- \[x] Project creation

\- \[x] Project persistence

\- \[x] AI requirement understanding

\- \[x] AI technical planning

\- \[x] AI application generation

\- \[x] AI application explanation

\- \[x] AI learning guide

\- \[x] FastAPI backend

\- \[x] Streamlit frontend

\- \[x] Hugging Face AI integration

\- \[x] Supabase PostgreSQL database

\- \[x] Row Level Security

\- \[x] Render backend deployment

\- \[x] Streamlit frontend deployment

\- \[x] Production authentication configuration



\---



\## Technologies Used



| Category | Technology |

|---|---|

| Programming Language | Python |

| Frontend | Streamlit |

| Backend | FastAPI |

| API Server | Uvicorn |

| Data Validation | Pydantic |

| Generative AI | Qwen3-4B-Instruct-2507 |

| AI Platform | Hugging Face Inference API |

| Database | Supabase PostgreSQL |

| Authentication | Supabase Auth |

| Database Security | PostgreSQL Row Level Security |

| Source Control | Git / GitHub |

| Backend Deployment | Render |

| Frontend Deployment | Streamlit Community Cloud |



\---



\## Conclusion



AI App Builder demonstrates a practical approach to AI-assisted application development where generative AI participates in multiple stages of the software development lifecycle.



Rather than treating AI as a simple code generator, the prototype combines:



Understanding + Planning + Building + Explaining + Learning



into a single development workflow.



The project demonstrates how modern generative AI APIs can be integrated with a web application, backend API, authentication system, database, and cloud deployment to create a complete AI-powered development experience.



\---



\## Author



Pon Lakshman



B.Sc. (Honours) Data Science and Artificial Intelligence



Indian Institute of Technology Guwahati

