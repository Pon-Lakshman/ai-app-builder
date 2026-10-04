import streamlit as st
from core.supabase_client import get_supabase_client


st.set_page_config(
    page_title="AI App Builder",
    page_icon="🚀",
    layout="wide",
)


supabase = get_supabase_client()


# -----------------------------
# Authentication
# -----------------------------

if "user" not in st.session_state:
    st.session_state.user = None


if st.session_state.user is None:

    st.title("🚀 AI App Builder")
    st.subheader("AI-powered application development workspace")

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    # -------------------------
    # Sign In
    # -------------------------

    with tab1:
        st.markdown("### Welcome back")

        email = st.text_input(
            "Email",
            key="signin_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signin_password"
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True
        ):
            if not email or not password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password(
                        {
                            "email": email,
                            "password": password,
                        }
                    )

                    st.session_state.user = response.user

                    st.success("Signed in successfully!")
                    st.rerun()

                except Exception as e:
                    st.error("Sign in failed.")
                    st.error(str(e))

    # -------------------------
    # Sign Up
    # -------------------------

    with tab2:
        st.markdown("### Create your account")

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):
            if not signup_email or not signup_password:
                st.warning("Please enter your email and password.")
            elif len(signup_password) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                try:
                    response = supabase.auth.sign_up(
                        {
                            "email": signup_email,
                            "password": signup_password,
                        }
                    )

                    if response.user:
                        st.success(
                            "Account created! "
                            "Check your email if confirmation is required."
                        )

                except Exception as e:
                    st.error("Account creation failed.")
                    st.error(str(e))


else:

    # -----------------------------
    # Logged-in Dashboard
    # -----------------------------

    user = st.session_state.user

    st.title("🚀 AI App Builder")

    st.write(
        f"Welcome back, **{user.email}** 👋"
    )

    st.divider()

    st.subheader("Your Workspace")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "🧠 Understand\n\n"
            "Turn your app idea into clear requirements."
        )

    with col2:
        st.info(
            "🗺️ Plan\n\n"
            "Create an architecture and development plan."
        )

    col3, col4 = st.columns(2)

    with col3:
        st.info(
            "🛠️ Build\n\n"
            "Generate the application structure and code."
        )

    with col4:
        st.info(
            "🎓 Explain & Learn\n\n"
            "Understand the generated application."
        )

    st.divider()

    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()