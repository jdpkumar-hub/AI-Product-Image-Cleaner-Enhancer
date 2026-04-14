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

# =========================================================
# 🔐 AUTH SECTION
# =========================================================
if not st.session_state.user:

    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    # ---------- LOGIN ----------
    if menu == "Login":
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            try:
                res = login(email, password)

                if res.user:
                    st.session_state.user = res.user
                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Invalid email or password")

            except Exception as e:
                st.error(f"Login failed: {str(e)}")

    # ---------- SIGNUP ----------
    elif menu == "Signup":
        st.subheader("Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            try:
                signup(email, password)
                st.success("Account created! Please verify your email.")
            except Exception:
                st.error("Signup failed")

# =========================================================
# 🚀 MAIN APP
# =========================================================
if st.session_state.user:

    st.sidebar.success(f"Welcome {st.session_state.user.email}")

    option = st.sidebar.radio("Menu", ["Enhance Image", "Logout"])

    # ---------- LOGOUT ----------
    if option == "Logout":
        st.session_state.user = None
        st.rerun()

    # ---------- ENHANCE IMAGE ----------
    if option == "Enhance Image":

        st.subheader("Upload & Enhance Image")

        # 🔥 Enhancement type
        enhance_type = st.selectbox(
            "Enhancement Type",
            ["Full Clean (Recommended)", "Only Enhance"]
        )

        uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if uploaded:
            img = Image.open(uploaded)

            col1, col2 = st.columns(2)

            with col1:
                st.image(img, caption="Original", use_column_width=True)

            if st.button("Enhance Image"):
                with st.spinner("Processing..."):

                    # 🔥 Apply enhancement
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