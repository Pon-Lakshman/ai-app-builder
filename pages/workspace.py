import json

import streamlit as st

from core.project_service import (
    get_user_projects,
    update_project_section,
)
from core.api_client import call_api


def parse_ai_json(response: str):
    """
    Extract and parse JSON from an AI response.

    Handles:
    - Normal JSON
    - ```json ... ``` responses
    - JSON surrounded by extra text
    """

    response = response.strip()

    # First attempt: response is already valid JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Remove Markdown code fences
    if response.startswith("```"):
        lines = response.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

    # Try extracting the JSON object from surrounding text
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:
        json_text = response[start:end + 1]

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

    # Nothing could be parsed
    return {
        "raw_response": response
    }


st.set_page_config(
    page_title="App Workspace",
    page_icon="🛠️",
    layout="wide",
)


# -----------------------------
# Authentication check
# -----------------------------

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please sign in first.")
    st.stop()


user = st.session_state.user


# -----------------------------
# Get selected project
# -----------------------------

if "selected_project_id" not in st.session_state:
    st.warning("Please select an app from the Dashboard.")
    st.stop()


project_id = st.session_state.selected_project_id


# -----------------------------
# Load project
# -----------------------------

projects = get_user_projects(user.id)

project = next(
    (p for p in projects if p["id"] == project_id),
    None,
)

if project is None:
    st.error("Project not found.")
    st.stop()


# -----------------------------
# Header
# -----------------------------

st.title(f"🛠️ {project['name']}")

st.caption("AI-powered application development workspace")

st.divider()


# -----------------------------
# Workflow
# -----------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🧠 Understand",
        "🗺️ Plan",
        "🛠️ Build",
        "💡 Explain",
        "🎓 Learn",
    ]
)


# =========================================================
# UNDERSTAND
# =========================================================

with tab1:

    st.subheader("🧠 Understand Your App")

    st.markdown(
        "Let's turn your idea into clear, structured requirements "
        "before writing any code."
    )

    st.markdown("### Your App Idea")

    st.info(project["prompt"])

    st.divider()

    if st.button(
        "🧠 Analyze My App Idea",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Understanding your application idea..."):

            try:

                # Call FastAPI instead of calling the LLM directly.
                understanding = call_api(
                    endpoint="/api/understand",
                    prompt=project["prompt"],
                )

                # The FastAPI endpoint already returns parsed JSON,
                # so no json.loads() is required here.

                update_project_section(
                    project_id=project_id,
                    user_id=user.id,
                    column="understanding",
                    value=understanding,
                )

                st.session_state.understanding = understanding

                st.success(
                    "Your application idea has been analyzed successfully."
                )

            except Exception as e:

                st.error("AI analysis failed.")
                st.error(str(e))

    # Display saved/current result

    understanding = st.session_state.get(
        "understanding",
        project.get("understanding"),
    )

    if understanding:

        st.divider()

        st.subheader("AI Understanding")

        if "raw_response" in understanding:

            st.write(understanding["raw_response"])

        else:

            if understanding.get("app_purpose"):
                st.markdown("### 🎯 App Purpose")
                st.write(understanding["app_purpose"])

            if understanding.get("target_users"):
                st.markdown("### 👥 Target Users")
                for item in understanding["target_users"]:
                    st.write(f"- {item}")

            if understanding.get("core_features"):
                st.markdown("### ⚙️ Core Features")
                for item in understanding["core_features"]:
                    st.write(f"- {item}")

            if understanding.get("user_flow"):
                st.markdown("### 🔄 User Flow")
                for index, item in enumerate(
                    understanding["user_flow"],
                    start=1,
                ):
                    st.write(f"{index}. {item}")

            if understanding.get("functional_requirements"):
                st.markdown("### 📋 Functional Requirements")
                for item in understanding["functional_requirements"]:
                    st.write(f"- {item}")

            if understanding.get("non_functional_requirements"):
                st.markdown("### 🛡️ Non-Functional Requirements")
                for item in understanding["non_functional_requirements"]:
                    st.write(f"- {item}")

            if understanding.get("suggested_technology"):
                st.markdown("### 💻 Suggested Technology")
                for item in understanding["suggested_technology"]:
                    st.write(f"- {item}")

            if understanding.get("potential_challenges"):
                st.markdown("### ⚠️ Potential Challenges")
                for item in understanding["potential_challenges"]:
                    st.write(f"- {item}")


# =========================================================
# PLAN
# =========================================================

with tab2:

    st.subheader("🗺️ Plan")

    st.markdown(
        "Turn the AI understanding into a practical architecture "
        "and step-by-step implementation plan."
    )

    # -----------------------------------------------------
    # Load AI Understanding
    # -----------------------------------------------------

    understanding = st.session_state.get(
        "understanding",
        project.get("understanding"),
    )

    if not understanding:

        st.warning(
            "Please complete the Understand stage first."
        )

    else:

        # -------------------------------------------------
        # Generate Development Plan
        # -------------------------------------------------

        if st.button(
            "🗺️ Generate Development Plan",
            type="primary",
            use_container_width=True,
        ):

            # Convert understanding into text for the API
            understanding_text = json.dumps(
                understanding,
                indent=2,
            )

            with st.spinner(
                "Designing your application architecture..."
            ):

                try:

                    # -------------------------------------
                    # Call FastAPI
                    # -------------------------------------

                    plan = call_api(
                        endpoint="/api/plan",
                        prompt=understanding_text,
                    )

                    # -------------------------------------
                    # Save plan to Supabase
                    # -------------------------------------

                    update_project_section(
                        project_id=project_id,
                        user_id=user.id,
                        column="plan",
                        value=plan,
                    )

                    # -------------------------------------
                    # Save plan in Streamlit session
                    # -------------------------------------

                    st.session_state.plan = plan

                    st.success(
                        "Development plan generated successfully."
                    )

                except Exception as e:

                    st.error(
                        "Plan generation failed."
                    )

                    st.error(str(e))

        # -------------------------------------------------
        # Load Saved / Current Plan
        # -------------------------------------------------

        plan = st.session_state.get(
            "plan",
            project.get("plan"),
        )

        # -------------------------------------------------
        # Display Plan
        # -------------------------------------------------

        if plan:

            st.divider()

            st.subheader("Application Plan")

            # ---------------------------------------------
            # Fallback if AI returned unstructured response
            # ---------------------------------------------

            if "raw_response" in plan:

                st.warning(
                    "The AI response could not be structured correctly."
                )

                st.write(
                    plan["raw_response"]
                )

            else:

                # -----------------------------------------
                # Architecture
                # -----------------------------------------

                if plan.get("architecture"):

                    st.markdown(
                        "### 🏗️ Architecture"
                    )

                    st.write(
                        plan["architecture"]
                    )

                # -----------------------------------------
                # Technology Stack
                # -----------------------------------------

                if plan.get("technology_stack"):

                    st.markdown(
                        "### 💻 Technology Stack"
                    )

                    for item in plan["technology_stack"]:

                        st.write(
                            f"- {item}"
                        )

                # -----------------------------------------
                # Database Design
                # -----------------------------------------

                if plan.get("database_design"):

                    st.markdown(
                        "### 🗄️ Database Design"
                    )

                    for item in plan["database_design"]:

                        st.write(
                            f"- {item}"
                        )

                # -----------------------------------------
                # Application Components
                # -----------------------------------------

                if plan.get("application_components"):

                    st.markdown(
                        "### 🧩 Application Components"
                    )

                    for item in plan[
                        "application_components"
                    ]:

                        st.write(
                            f"- {item}"
                        )

                # -----------------------------------------
                # API Design
                # -----------------------------------------

                if plan.get("api_design"):

                    st.markdown(
                        "### 🔌 API Design"
                    )

                    for item in plan["api_design"]:

                        st.write(
                            f"- {item}"
                        )

                # -----------------------------------------
                # Development Phases
                # -----------------------------------------

                if plan.get("development_phases"):

                    st.markdown(
                        "### 🛠️ Development Phases"
                    )

                    for index, item in enumerate(
                        plan["development_phases"],
                        start=1,
                    ):

                        st.write(
                            f"{index}. {item}"
                        )

                # -----------------------------------------
                # Security Considerations
                # -----------------------------------------

                if plan.get(
                    "security_considerations"
                ):

                    st.markdown(
                        "### 🔐 Security Considerations"
                    )

                    for item in plan[
                        "security_considerations"
                    ]:

                        st.write(
                            f"- {item}"
                        )

                # -----------------------------------------
                # Deployment Plan
                # -----------------------------------------

                if plan.get("deployment_plan"):

                    st.markdown(
                        "### 🚀 Deployment Plan"
                    )

                    deployment_plan = plan.get("deployment_plan", [])

                    if isinstance(deployment_plan, list):
                        for item in deployment_plan:
                            st.markdown(f"- {item}")
                    else:
                        st.write(deployment_plan)

# =========================================================
# BUILD
# =========================================================

with tab3:

    st.subheader("🛠️ Build")

    st.write(
        "AI will build a runnable MVP from the approved development plan."
    )

    # -----------------------------------------------------
    # Load Understanding and Plan
    # -----------------------------------------------------

    understanding = st.session_state.get(
        "understanding",
        project.get("understanding"),
    )

    plan = st.session_state.get(
        "plan",
        project.get("plan"),
    )

    if not understanding:

        st.warning(
            "Please complete the Understand step first."
        )

    elif not plan:

        st.warning(
            "Please complete the Plan step first."
        )

    else:

        # -------------------------------------------------
        # Build Application
        # -------------------------------------------------

        if st.button(
            "🛠️ Build Application",
            type="primary",
            use_container_width=True,
        ):

            # ---------------------------------------------
            # Prepare Build Request
            # ---------------------------------------------

            build_input = {
                "user_request": project["prompt"],
                "understanding": understanding,
                "development_plan": plan,
            }

            build_input_text = json.dumps(
                build_input,
                indent=2,
            )

            with st.spinner(
                "Building your application..."
            ):

                try:

                    # -------------------------------------
                    # Call FastAPI
                    # -------------------------------------

                    generated_code = call_api(
                        endpoint="/api/build",
                        prompt=build_input_text,
                        timeout=600,
                    )

                    # -------------------------------------
                    # Save in session
                    # -------------------------------------

                    st.session_state.generated_code = (
                        generated_code
                    )

                    # -------------------------------------
                    # Save to Supabase
                    # -------------------------------------

                    try:

                        update_project_section(
                            project_id=project_id,
                            user_id=user.id,
                            column="generated_code",
                            value=generated_code,
                        )

                    except Exception as e:

                        st.warning(
                            "Application was generated, "
                            "but saving to the database failed."
                        )

                        st.warning(str(e))

                    st.success(
                        "Application built successfully."
                    )

                except Exception as e:

                    st.error(
                        "Application build failed."
                    )

                    st.error(str(e))

        # -------------------------------------------------
        # Load Existing Generated Application
        # -------------------------------------------------

        generated_code = st.session_state.get(
            "generated_code",
            project.get("generated_code"),
        )

        # -------------------------------------------------
        # Display Generated Application
        # -------------------------------------------------

        if generated_code:

            st.divider()

            st.subheader(
                "Generated Application"
            )

            # ---------------------------------------------
            # Project information
            # ---------------------------------------------

            st.write(
                f"**Project:** "
                f"{generated_code.get('project_name', 'Generated Application')}"
            )

            files = generated_code.get(
                "files",
                [],
            )

            st.write(
                f"**Files generated:** "
                f"{len(files)}"
            )

            # ---------------------------------------------
            # Technology Stack
            # ---------------------------------------------

            technology_stack = generated_code.get(
                "technology_stack",
                [],
            )

            if technology_stack:

                st.markdown(
                    "### 💻 Technology Stack"
                )

                st.write(
                    ", ".join(
                        str(item)
                        for item in technology_stack
                    )
                )

            # ---------------------------------------------
            # Generated Files
            # ---------------------------------------------

            if files:

                st.markdown(
                    "### 📂 Generated Files"
                )

                for file_info in files:

                    filename = file_info.get(
                        "filename",
                        "unknown",
                    )

                    purpose = file_info.get(
                        "purpose",
                        "",
                    )

                    code = file_info.get(
                        "code",
                        "",
                    )

                    st.markdown(
                        f"#### `{filename}`"
                    )

                    if purpose:

                        st.caption(
                            purpose
                        )

                    # -------------------------------------
                    # Syntax highlighting
                    # -------------------------------------

                    extension = (
                        filename.lower()
                        .split(".")[-1]
                    )

                    language_map = {
                        "py": "python",
                        "js": "javascript",
                        "jsx": "javascript",
                        "ts": "typescript",
                        "tsx": "typescript",
                        "json": "json",
                        "html": "html",
                        "css": "css",
                        "sql": "sql",
                        "md": "markdown",
                        "yaml": "yaml",
                        "yml": "yaml",
                        "sh": "bash",
                        "txt": "text",
                    }

                    language = language_map.get(
                        extension,
                        "text",
                    )

                    st.code(
                        code,
                        language=language,
                    )

            # ---------------------------------------------
            # Run Instructions
            # ---------------------------------------------

            run_instructions = generated_code.get(
                "run_instructions",
                [],
            )

            if run_instructions:

                st.markdown(
                    "### ▶️ Run Instructions"
                )

                for index, instruction in enumerate(
                    run_instructions,
                    start=1,
                ):

                    st.write(
                        f"{index}. {instruction}"
                    )


# =========================================================
# EXPLAIN
# =========================================================

with tab4:

    st.subheader("💡 Explain Your Application")

    st.write(
        "Understand how the generated application works, "
        "file by file and component by component."
    )

    # -----------------------------------------------------
    # Load Generated Application
    # -----------------------------------------------------

    generated_code = st.session_state.get(
        "generated_code",
        project.get("generated_code"),
    )

    if not generated_code:

        st.warning(
            "Please complete the Build stage first."
        )

    else:

        # -------------------------------------------------
        # Generate Explanation
        # -------------------------------------------------

        if st.button(
            "💡 Explain My Application",
            type="primary",
            use_container_width=True,
        ):

            explanation_input = {
                "user_request": project["prompt"],
                "generated_application": generated_code,
            }

            explanation_input_text = json.dumps(
                explanation_input,
                indent=2,
            )

            with st.spinner(
                "Analyzing your application and preparing an explanation..."
            ):

                try:

                    # -------------------------------------
                    # Call FastAPI
                    # -------------------------------------

                    explanation = call_api(
                        endpoint="/api/explain",
                        prompt=explanation_input_text,
                        timeout=300,
                    )

                    # -------------------------------------
                    # Save to Supabase
                    # -------------------------------------

                    update_project_section(
                        project_id=project_id,
                        user_id=user.id,
                        column="explanation",
                        value=explanation,
                    )

                    # -------------------------------------
                    # Save to Streamlit session
                    # -------------------------------------

                    st.session_state.explanation = (
                        explanation
                    )

                    st.success(
                        "Application explanation generated successfully."
                    )

                except Exception as e:

                    st.error(
                        "Explanation generation failed."
                    )

                    st.error(str(e))

        # -------------------------------------------------
        # Load Saved Explanation
        # -------------------------------------------------

        explanation = st.session_state.get(
            "explanation",
            project.get("explanation"),
        )

        # -------------------------------------------------
        # Display Explanation
        # -------------------------------------------------

        if explanation:

            # ---------------------------------------------
            # Fallback
            # ---------------------------------------------

            if "raw_response" in explanation:

                st.warning(
                    "The AI response could not be structured correctly."
                )

                st.write(
                    explanation["raw_response"]
                )

            else:

                # -----------------------------------------
                # Application Overview
                # -----------------------------------------

                st.markdown(
                    "### 📱 Application Overview"
                )

                st.write(
                    explanation.get(
                        "application_overview",
                        "No overview available.",
                    )
                )

                st.divider()

                # -----------------------------------------
                # Architecture
                # -----------------------------------------

                st.markdown(
                    "### 🏗️ Architecture"
                )

                st.write(
                    explanation.get(
                        "architecture_explanation",
                        "No architecture explanation available.",
                    )
                )

                st.divider()

                # -----------------------------------------
                # Technologies
                # -----------------------------------------

                st.markdown(
                    "### ⚙️ Technologies Used"
                )

                technologies = explanation.get(
                    "technology_explanation",
                    [],
                )

                if technologies:

                    for technology in technologies:

                        st.markdown(
                            f"- {technology}"
                        )

                else:

                    st.info(
                        "No technology explanation available."
                    )

                st.divider()

                # -----------------------------------------
                # File-by-File Explanation
                # -----------------------------------------

                st.markdown(
                    "### 📂 File-by-File Explanation"
                )

                file_explanations = explanation.get(
                    "file_explanations",
                    [],
                )

                if file_explanations:

                    for file_info in file_explanations:

                        filename = file_info.get(
                            "filename",
                            "Unknown file",
                        )

                        purpose = file_info.get(
                            "purpose",
                            "",
                        )

                        how_it_works = file_info.get(
                            "how_it_works",
                            "",
                        )

                        with st.expander(
                            f"📄 {filename}"
                        ):

                            st.markdown(
                                "**Purpose**"
                            )

                            st.write(
                                purpose
                            )

                            st.markdown(
                                "**How it works**"
                            )

                            st.write(
                                how_it_works
                            )

                else:

                    st.info(
                        "No file explanations available."
                    )

                st.divider()

                # -----------------------------------------
                # Application Flow
                # -----------------------------------------

                st.markdown(
                    "### 🔄 Application Flow"
                )

                application_flow = explanation.get(
                    "application_flow",
                    [],
                )

                if application_flow:

                    for index, step in enumerate(
                        application_flow,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}.** {step}"
                        )

                else:

                    st.info(
                        "No application flow available."
                    )

                st.divider()

                # -----------------------------------------
                # Important Concepts
                # -----------------------------------------

                st.markdown(
                    "### 🧠 Important Concepts"
                )

                important_concepts = explanation.get(
                    "important_concepts",
                    [],
                )

                if important_concepts:

                    for concept in important_concepts:

                        st.markdown(
                            f"- {concept}"
                        )

                else:

                    st.info(
                        "No important concepts available."
                    )

                st.divider()

                # -----------------------------------------
                # Data Flow
                # -----------------------------------------

                st.markdown(
                    "### 🔀 Data Flow"
                )

                st.write(
                    explanation.get(
                        "data_flow",
                        "No data flow explanation available.",
                    )
                )

                st.divider()

                # -----------------------------------------
                # Key Takeaways
                # -----------------------------------------

                st.markdown(
                    "### 🎯 Key Takeaways"
                )

                key_takeaways = explanation.get(
                    "key_takeaways",
                    [],
                )

                if key_takeaways:

                    for takeaway in key_takeaways:

                        st.markdown(
                            f"- {takeaway}"
                        )

                else:

                    st.info(
                        "No key takeaways available."
                    )


# =========================================================
# LEARN
# =========================================================

with tab5:

    st.subheader("🎓 Learn From Your Application")

    st.write(
        "Understand the technologies behind your application, "
        "practice the concepts, and discover what to build next."
    )

    # -----------------------------------------------------
    # Load Required Project Data
    # -----------------------------------------------------

    plan = st.session_state.get(
        "plan",
        project.get("plan"),
    )

    explanation = st.session_state.get(
        "explanation",
        project.get("explanation"),
    )

    generated_code = st.session_state.get(
        "generated_code",
        project.get("generated_code"),
    )

    # -----------------------------------------------------
    # Check Workflow Requirements
    # -----------------------------------------------------

    if not generated_code:

        st.warning(
            "Please complete the Build stage first."
        )

    elif not explanation:

        st.warning(
            "Please complete the Explain stage first."
        )

    else:

        # -------------------------------------------------
        # Generate Learning Guide
        # -------------------------------------------------

        if st.button(
            "🎓 Create My Learning Guide",
            type="primary",
            use_container_width=True,
        ):

            learning_input = {
                "user_request": project["prompt"],
                "technology_stack": plan.get(
                    "technology_stack",
                    [],
                ) if plan else [],
                "application_explanation": explanation,
            }

            learning_input_text = json.dumps(
                learning_input,
                indent=2,
            )

            with st.spinner(
                "Creating your personalized learning guide..."
            ):

                try:

                    # -------------------------------------
                    # Call FastAPI
                    # -------------------------------------

                    learning_content = call_api(
                        endpoint="/api/learn",
                        prompt=learning_input_text,
                        timeout=300,
                    )

                    # -------------------------------------
                    # Save to Supabase
                    # -------------------------------------

                    update_project_section(
                        project_id=project_id,
                        user_id=user.id,
                        column="learning_content",
                        value=learning_content,
                    )

                    # -------------------------------------
                    # Save to Streamlit Session
                    # -------------------------------------

                    st.session_state.learning_content = (
                        learning_content
                    )

                    st.success(
                        "Your learning guide is ready."
                    )

                except Exception as e:

                    st.error(
                        "Learning guide generation failed."
                    )

                    st.error(str(e))

        # -------------------------------------------------
        # Load Saved Learning Content
        # -------------------------------------------------

        learning_content = st.session_state.get(
            "learning_content",
            project.get("learning_content"),
        )

        # -------------------------------------------------
        # Display Learning Guide
        # -------------------------------------------------

        if learning_content:

            # ---------------------------------------------
            # Fallback
            # ---------------------------------------------

            if "raw_response" in learning_content:

                st.warning(
                    "The AI response could not be structured correctly."
                )

                st.markdown(
                    learning_content["raw_response"]
                )

            else:

                # -----------------------------------------
                # Learning Overview
                # -----------------------------------------

                st.markdown(
                    "### 📚 Learning Overview"
                )

                st.info(
                    learning_content.get(
                        "learning_overview",
                        "No learning overview available.",
                    )
                )

                st.divider()

                # -----------------------------------------
                # Technologies
                # -----------------------------------------

                st.markdown(
                    "### ⚙️ Technologies to Learn"
                )

                technologies = learning_content.get(
                    "technologies_to_learn",
                    [],
                )

                if technologies:

                    for technology in technologies:

                        name = technology.get(
                            "technology",
                            "Technology",
                        )

                        with st.expander(
                            f"🔧 {name}"
                        ):

                            st.markdown(
                                "**Why it is used**"
                            )

                            st.write(
                                technology.get(
                                    "why_it_is_used",
                                    "",
                                )
                            )

                            st.markdown(
                                "**What to learn**"
                            )

                            topics = technology.get(
                                "what_to_learn",
                                [],
                            )

                            for topic in topics:

                                st.markdown(
                                    f"- {topic}"
                                )

                else:

                    st.info(
                        "No technologies were identified."
                    )

                st.divider()

                # -----------------------------------------
                # Core Concepts
                # -----------------------------------------

                st.markdown(
                    "### 🧠 Core Concepts"
                )

                concepts = learning_content.get(
                    "core_concepts",
                    [],
                )

                if concepts:

                    for concept in concepts:

                        name = concept.get(
                            "concept",
                            "Concept",
                        )

                        with st.expander(
                            f"🧠 {name}"
                        ):

                            st.markdown(
                                "**What it means**"
                            )

                            st.write(
                                concept.get(
                                    "explanation",
                                    "",
                                )
                            )

                            st.markdown(
                                "**Why it matters**"
                            )

                            st.write(
                                concept.get(
                                    "why_it_matters",
                                    "",
                                )
                            )

                else:

                    st.info(
                        "No core concepts were identified."
                    )

                st.divider()

                # -----------------------------------------
                # Learning Path
                # -----------------------------------------

                st.markdown(
                    "### 🪜 Learning Path"
                )

                learning_path = learning_content.get(
                    "learning_path",
                    [],
                )

                if learning_path:

                    for index, step in enumerate(
                        learning_path,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}.** {step}"
                        )

                else:

                    st.info(
                        "No learning path available."
                    )

                st.divider()

                # -----------------------------------------
                # Practice Tasks
                # -----------------------------------------

                st.markdown(
                    "### 🧪 Practice Tasks"
                )

                practice_tasks = learning_content.get(
                    "practice_tasks",
                    [],
                )

                if practice_tasks:

                    for index, task in enumerate(
                        practice_tasks,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}.** {task}"
                        )

                else:

                    st.info(
                        "No practice tasks available."
                    )

                st.divider()

                # -----------------------------------------
                # Next Improvements
                # -----------------------------------------

                st.markdown(
                    "### 🚀 What You Can Build Next"
                )

                next_improvements = learning_content.get(
                    "next_improvements",
                    [],
                )

                if next_improvements:

                    for improvement in next_improvements:

                        st.markdown(
                            f"- {improvement}"
                        )

                else:

                    st.info(
                        "No next improvements available."
                    )

                st.divider()

                # -----------------------------------------
                # Challenge Questions
                # -----------------------------------------

                st.markdown(
                    "### ❓ Test Your Understanding"
                )

                challenge_questions = learning_content.get(
                    "challenge_questions",
                    [],
                )

                if challenge_questions:

                    for index, question in enumerate(
                        challenge_questions,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}.** {question}"
                        )

                else:

                    st.info(
                        "No challenge questions available."
                    )

                st.divider()

                # -----------------------------------------
                # Skills Gained
                # -----------------------------------------

                st.markdown(
                    "### 🎯 Skills Gained"
                )

                skills_gained = learning_content.get(
                    "skills_gained",
                    [],
                )

                if skills_gained:

                    for skill in skills_gained:

                        st.markdown(
                            f"- {skill}"
                        )

                else:

                    st.info(
                        "No skills were identified."
                    )