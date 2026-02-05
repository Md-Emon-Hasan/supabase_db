import os
from flask import Flask, request, redirect
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

# 🟢 Home page → HTML Form
@app.route("/", methods=["GET"])
def home():
    return """
    <h2>Create User</h2>
    <form method="POST" action="/users">
        <input type="text" name="first_name" placeholder="First Name" required />
        <br><br>
        <input type="text" name="last_name" placeholder="Last Name" required />
        <br><br>
        <input type="number" name="age" placeholder="Age" required />
        <br><br>
        <button type="submit">Save</button>
    </form>
    <br>
    <a href="/users">View All Users</a>
    """

# 🟢 Insert user (from browser)
@app.route("/users", methods=["POST"])
def create_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")

    supabase.table("users").insert({
        "first_name": first_name,
        "last_name": last_name,
        "age": int(age)
    }).execute()

    return redirect("/users")

# 🟢 Show all users
@app.route("/users", methods=["GET"])
def get_users():
    response = supabase.table("users").select("*").execute()

    html = "<h2>Users List</h2><ul>"
    for user in response.data:
        html += f"<li>{user['first_name']} {user['last_name']} — Age: {user['age']}</li>"
    html += "</ul><br><a href='/'>Add New User</a>"

    return html


if __name__ == "__main__":
    app.run(debug=True)
