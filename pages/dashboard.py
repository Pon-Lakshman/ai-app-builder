import streamlit as st

from core.project_service import create_project, get_user_projects


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI App Builder",
    page_icon="🚀",
    layout="wide",
)


# -----------------------------
# Authentication Check
# -----------------------------

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please sign in first.")
    st.stop()

user = st.session_state.user


# -----------------------------
# Header
# -----------------------------

st.title("🚀 AI App Builder")

st.write(f"Welcome back, **{user.email}** 👋")

st.divider()


# -----------------------------
# Create New App
# -----------------------------

st.subheader("✨ Create a New App")

project_name = st.text_input(
    "App Name",
    placeholder="Example: Personal Expense Tracker",
)

project_prompt = st.text_area(
    "Describe your app idea",
    placeholder=(
        "Example: I want to build a personal expense tracker "
        "where users can add expenses, categorize them, "
        "view monthly spending, and see charts."
    ),
    height=150,
)


if st.button(
    "Create App",
    type="primary",
    use_container_width=True,
):

    if not project_name.strip():
        st.warning("Please enter an app name.")

    elif not project_prompt.strip():
        st.warning("Please describe your app idea.")

    else:
        try:
            create_project(
                user_id=user.id,
                name=project_name.strip(),
                prompt=project_prompt.strip(),
            )

            st.success("App created successfully! 🎉")

            st.rerun()

        except Exception as e:
            st.error("Failed to create the app.")
            st.error(str(e))


st.divider()


# -----------------------------
# Existing Projects
# -----------------------------

st.subheader("📂 Your Apps")

try:

    projects = get_user_projects(user.id)

    if not projects:

        st.info(
            "You haven't created any apps yet. "
            "Create your first app above."
        )

    else:

        for project in projects:

            with st.container(border=True):

                st.markdown(
                    f"### 🛠️ {project['name']}"
                )

                st.write(project["prompt"])

                st.caption(
                    f"Last updated: {project['updated_at']}"
                )

                if st.button(
                    "Open Workspace",
                    key=f"open_{project['id']}",
                    use_container_width=True,
                ):

                    st.session_state.selected_project_id = project["id"]

                    st.switch_page(
                        "pages/workspace.py"
                    )

except Exception as e:

    st.error("Could not load your apps.")
    st.error(str(e))