from core.supabase_client import get_supabase_client


def create_project(user_id: str, name: str, prompt: str):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("projects")
        .insert({
            "user_id": user_id,
            "name": name,
            "prompt": prompt,
        })
        .execute()
    )

    return response.data


def get_user_projects(user_id: str):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("projects")
        .select("*")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )

    return response.data

def update_project_section(
    project_id: str,
    user_id: str,
    column: str,
    value,
):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("projects")
        .update({
            column: value,
            "updated_at": "now()",
        })
        .eq("id", project_id)
        .eq("user_id", user_id)
        .execute()
    )

    return response.data