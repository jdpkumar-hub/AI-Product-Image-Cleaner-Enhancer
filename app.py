import streamlit as st
from PIL import Image
from auth import login, signup
from enhance import enhance_image

st.set_page_config(page_title="AI Image Enhancer", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1 {
    text-align: center;
}
.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #00C9A7);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Image Enhancer SaaS")

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None
    
if "email" not in st.session_state:
    st.session_state.email = ""

if "password" not in st.session_state:
    st.session_state.password = ""
# =========================================================
# 🔐 AUTH SECTION (ONLY WHEN NOT LOGGED IN)
# =========================================================
if not st.session_state.user:

    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    # ---------- LOGIN ----------
email = st.text_input("Email")
password = st.text_input("Password", type="password")

login_btn = st.button("Login")

if login_btn:
    try:
        res = login(email, password)

        if res.user:
            st.session_state.user = res.user

            # 🔥 Clear form inputs
            st.session_state["email"] = ""
            st.session_state["password"] = ""

            # 🔥 Stop execution immediately
            st.success("Login successful!")
            st.stop()

        else:
            st.error("Invalid email or password")

    except Exception as e:
        st.error("Login failed")

    # ---------- SIGNUP ----------
    elif menu == "Signup":
        st.subheader("Create Account")

        email = st.text_input("Email ")
        password = st.text_input("Password ", type="password")

        if st.button("Signup"):
            try:
                signup(email, password)
                st.success("Account created! Please login.")
            except:
                st.error("Signup failed")

# =========================================================
# 🚀 MAIN APP (ONLY WHEN LOGGED IN)
# =========================================================
else:

    st.sidebar.success(f"Welcome {st.session_state.user.email}")

    option = st.sidebar.radio("Menu", ["Enhance Image", "Logout"])

    # ---------- LOGOUT ----------
    if option == "Logout":
        st.session_state.user = None
        st.rerun()

    # ---------- ENHANCE IMAGE ----------
    if option == "Enhance Image":

        st.subheader("Upload & Enhance Image")

        uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if uploaded:
            img = Image.open(uploaded)

            col1, col2 = st.columns(2)

            with col1:
                st.image(img, caption="Original", use_column_width=True)

            if st.button("Enhance Image"):
                with st.spinner("Processing..."):
                    result = enhance_image(img)

                with col2:
                    st.image(result, caption="Enhanced", use_column_width=True)

                result.save("output.png")

                with open("output.png", "rb") as f:
                    st.download_button(
                        "Download Enhanced Image",
                        f,
                        file_name="enhanced.png"
                    )