import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Users API")

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

# ---------- Schemas ----------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    age: int


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None


# ---------- Health ----------
@app.get("/")
def health():
    return {"status": "API is running"}


# ---------- Create ----------
@app.post("/users")
def create_user(user: UserCreate):
    response = supabase.table("users").insert(user.dict()).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Insert failed")

    return response.data[0]


# ---------- Read All ----------
@app.get("/users")
def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data


# ---------- Read One ----------
@app.get("/users/{user_id}")
def get_user(user_id: str):
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")

    return response.data


# ---------- Update ----------
@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    response = (
        supabase
        .table("users")
        .update(user.dict(exclude_unset=True))
        .eq("id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Update failed")

    return response.data[0]


# ---------- Delete ----------
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    response = (
        supabase
        .table("users")
        .delete()
        .eq("id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Delete failed")

    return {"message": "User deleted successfully"}
