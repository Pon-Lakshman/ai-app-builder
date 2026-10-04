import json

from fastapi import APIRouter, HTTPException

from api.schemas import AppRequest, AppResponse
from core.llm import generate_response
from core.json_utils import parse_ai_json

router = APIRouter(
    prefix="/api",
    tags=["AI App Development"],
)

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI App Builder API"
    }

@router.post("/understand", response_model=AppResponse)
def understand_app(request: AppRequest):

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="App prompt cannot be empty.",
        )

    system_prompt = """
You are an AI software architect helping a user understand an application idea.

Analyze the user's application request and return ONLY valid JSON.

Use exactly these keys:

{
  "app_purpose": "",
  "target_users": [],
  "core_features": [],
  "user_flow": [],
  "functional_requirements": [],
  "non_functional_requirements": [],
  "suggested_technology": [],
  "potential_challenges": []
}

Do not include markdown.
Do not include explanations outside the JSON.
"""

    try:
        response = generate_response(
            system_prompt=system_prompt,
            user_prompt=request.prompt,
            max_tokens=800,
        )

        response = response.strip()

        # Remove markdown code fences if the model adds them.
        if response.startswith("```"):
            lines = response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            response = "\n".join(lines).strip()

        # Extract JSON if additional text was returned.
        try:
            result = json.loads(response)
        except json.JSONDecodeError:

            start = response.find("{")
            end = response.rfind("}")

            if start == -1 or end == -1:
                raise HTTPException(
                    status_code=500,
                    detail="AI returned an invalid JSON response.",
                )

            result = json.loads(
                response[start:end + 1]
            )

        return {
            "result": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(e)}",
        )


@router.post("/plan", response_model=AppResponse)
def plan_app(request: AppRequest):

    system_prompt = """
You are a senior software architect helping a developer
turn an application's requirements into a practical technical plan.

Return ONLY valid JSON.

Use exactly this structure:

{
  "architecture": "",
  "technology_stack": [],
  "database_design": [],
  "application_components": [],
  "api_design": [],
  "development_phases": [],
  "security_considerations": [],
  "deployment_plan": []
}

Rules:

- Keep the plan realistic for an MVP/prototype.
- Base the plan ONLY on the provided application understanding.
- Do not invent unnecessary technologies.
- Keep the technology stack consistent with the application requirements.
- If a backend API is not required, clearly say so.
- Do not introduce React, Node.js, Firebase, MongoDB, Docker,
  or other technologies unless the requirements justify them.
- Keep each list concise.
- Do not include Markdown.
- Do not include ```json.
- Return ONLY the JSON object.
"""

    try:

        response = generate_response(
            system_prompt=system_prompt,
            user_prompt=request.prompt,
            max_tokens=1400,
        )

        result = parse_ai_json(response)

        return {
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Plan generation failed: {str(e)}",
        )


@router.post("/build", response_model=AppResponse)
def build_app(request: AppRequest):

    # ---------------------------------------------------------
    # STEP 1 — Generate a small file manifest
    # ---------------------------------------------------------

    manifest_system = """
You are an expert software architect.

Your job is to convert an application plan into the smallest
possible set of files required for a runnable MVP.

Rules:

- Follow the provided technology stack exactly.
- Do NOT invent technologies that are not in the plan.
- Prefer a simple architecture.
- For small applications, prefer 1-5 files.
- Maximum 6 files.
- Every file must be genuinely necessary.
- The final application must be runnable.
- Do not create unnecessary frontend/backend separation.
- Do not add Docker, React, Node.js, MongoDB, Firebase, etc.
  unless explicitly required by the development plan.

Return ONLY valid JSON.

Format:

{
  "project_name": "",
  "project_description": "",
  "technology_stack": [],
  "files": [
    {
      "filename": "",
      "purpose": ""
    }
  ],
  "run_instructions": []
}
"""

    try:

        manifest_raw = generate_response(
            system_prompt=manifest_system,
            user_prompt=request.prompt,
            max_tokens=1400,
        )

        manifest = parse_ai_json(manifest_raw)

        if "raw_response" in manifest:

            raise ValueError(
                "AI did not return a valid application file manifest."
            )

        files_plan = manifest.get("files", [])

        if not files_plan:

            raise ValueError(
                "The AI did not produce any application files."
            )

        # Safety limit
        files_plan = files_plan[:6]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Build manifest generation failed: {str(e)}",
        )

    # ---------------------------------------------------------
    # STEP 2 — Generate each file independently
    # ---------------------------------------------------------

    generated_files = []

    for file_info in files_plan:

        filename = file_info.get(
            "filename",
            "",
        ).strip()

        purpose = file_info.get(
            "purpose",
            "",
        ).strip()

        if not filename:
            continue

        file_system = """
You are an expert software engineer.

Generate ONE complete production-quality MVP source file.

IMPORTANT RULES:

1. Generate the COMPLETE file.
2. Never truncate the file.
3. Never use placeholders such as:
   - TODO
   - "add code here"
   - "..."
   - "rest of code"
   - "implement this"
4. Do not explain the code outside the file.
5. Return ONLY the source code.
6. Follow the approved technology stack exactly.
7. Do not introduce new frameworks or databases.
8. Keep the application small and coherent.
9. The file must work with the other files in the provided manifest.
10. Make imports match the actual filenames in the manifest.
11. Do not generate files that are not requested.
"""

        file_user = f"""
APP NAME:
{manifest.get("project_name", "")}

APP DESCRIPTION:
{manifest.get("project_description", "")}

APPLICATION REQUEST:
{request.prompt}

APPROVED TECHNOLOGY STACK:
{json.dumps(manifest.get("technology_stack", []), indent=2)}

COMPLETE FILE MANIFEST:
{json.dumps(files_plan, indent=2)}

CURRENT FILE TO GENERATE:

Filename:
{filename}

Purpose:
{purpose}

Generate the COMPLETE contents of `{filename}`.

Do not return Markdown fences.
Do not return explanations.
Return only the file contents.
"""

        try:

            file_code = generate_response(
                system_prompt=file_system,
                user_prompt=file_user,
                max_tokens=2200,
            )

            file_code = file_code.strip()

            # Remove accidental Markdown code fences
            if file_code.startswith("```"):

                lines = file_code.splitlines()

                if lines:
                    lines = lines[1:]

                if (
                    lines
                    and lines[-1].strip() == "```"
                ):
                    lines = lines[:-1]

                file_code = "\n".join(
                    lines
                ).strip()

            generated_files.append(
                {
                    "filename": filename,
                    "purpose": purpose,
                    "code": file_code,
                }
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Failed to generate "
                    f"`{filename}`: {str(e)}"
                ),
            )

    # ---------------------------------------------------------
    # STEP 3 — Validate that files were generated
    # ---------------------------------------------------------

    if not generated_files:

        raise HTTPException(
            status_code=500,
            detail="No application files were generated.",
        )

    # ---------------------------------------------------------
    # STEP 4 — Assemble final application
    # ---------------------------------------------------------

    generated_code = {
        "project_name": manifest.get(
            "project_name",
            "Generated Application",
        ),
        "project_description": manifest.get(
            "project_description",
            "",
        ),
        "technology_stack": manifest.get(
            "technology_stack",
            [],
        ),
        "project_structure": files_plan,
        "files": generated_files,
        "run_instructions": manifest.get(
            "run_instructions",
            [],
        ),
    }

    return {
        "result": generated_code
    }


@router.post("/explain", response_model=AppResponse)
def explain_app(request: AppRequest):

    system_prompt = """
You are an expert software engineer and technical educator.

The user has generated an application using an
AI-powered application development tool.

Your task is to explain the generated application clearly
so that a developer can understand how it works.

Return ONLY valid JSON with exactly these keys:

{
  "application_overview": "",
  "architecture_explanation": "",
  "technology_explanation": [],
  "file_explanations": [
    {
      "filename": "",
      "purpose": "",
      "how_it_works": ""
    }
  ],
  "application_flow": [],
  "important_concepts": [],
  "data_flow": "",
  "key_takeaways": []
}

Rules:

- Explain the existing generated application.
- Do not generate new code.
- Do not invent files or technologies.
- Explain the role of each generated file.
- Explain how the files interact.
- Explain the main application flow.
- Keep explanations practical and beginner-friendly.
- Do not include Markdown code fences.
- Return ONLY valid JSON.
"""

    try:

        response = generate_response(
            system_prompt=system_prompt,
            user_prompt=request.prompt,
            max_tokens=1800,
        )

        result = parse_ai_json(response)

        return {
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Explanation generation failed: {str(e)}",
        )
    

@router.post("/learn", response_model=AppResponse)
def learn_app(request: AppRequest):

    system_prompt = """
You are an expert software engineering teacher.

Create a concise learning guide based on the user's
application, technology stack, and application explanation.

Return ONLY valid JSON with exactly these keys:

{
  "learning_overview": "",
  "technologies_to_learn": [
    {
      "technology": "",
      "why_it_is_used": "",
      "what_to_learn": []
    }
  ],
  "core_concepts": [
    {
      "concept": "",
      "explanation": "",
      "why_it_matters": ""
    }
  ],
  "learning_path": [],
  "practice_tasks": [],
  "next_improvements": [],
  "challenge_questions": [],
  "skills_gained": []
}

Rules:

- Keep the guide concise.
- Recommend only technologies actually used by the application.
- Maximum 5 technologies.
- Maximum 5 core concepts.
- Maximum 6 learning-path steps.
- Maximum 5 practice tasks.
- Maximum 5 next improvements.
- Maximum 5 challenge questions.
- Maximum 6 skills gained.
- Each list item should be short and practical.
- Do not generate code.
- Do not introduce technologies that are not used.
- Do not include Markdown.
- Do not include ```json.
- Return ONLY valid JSON.
"""

    try:

        response = generate_response(
            system_prompt=system_prompt,
            user_prompt=request.prompt,
            max_tokens=1200,
        )

        result = parse_ai_json(response)

        return {
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Learning guide generation failed: {str(e)}",
        )