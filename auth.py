from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
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