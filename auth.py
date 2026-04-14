from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def login(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })