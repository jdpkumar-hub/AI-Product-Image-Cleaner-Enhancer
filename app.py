import streamlit as st
from PIL import Image
from auth import login, signup
from enhance import enhance_image
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

st.set_page_config(page_title="AI Image Cleaner", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.big-title {font-size:40px; font-weight:bold; text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">AI Image Enhancer SaaS</p>', unsafe_allow_html=True)

# ---------- AUTH ----------
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if "user" not in st.session_state:
    st.session_state.user = None

if menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = login(email, password)
        if res.user:
            st.session_state.user = res.user
            st.success("Logged in!")

elif menu == "Signup":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        signup(email, password)
        st.success("Account created!")

# ---------- MAIN APP ----------
if st.session_state.user:

    st.sidebar.success(f"Welcome {st.session_state.user.email}")

    option = st.sidebar.radio("Options", ["Enhance Image", "Upgrade"])

    if option == "Enhance Image":

        uploaded = st.file_uploader("Upload Image")

        if uploaded:
            img = Image.open(uploaded)

            col1, col2 = st.columns(2)

            with col1:
                st.image(img, caption="Original")

            if st.button("Enhance"):
                with st.spinner("Processing..."):
                    result = enhance_image(img)

                with col2:
                    st.image(result, caption="Enhanced")

                result.save("output.png")

                with open("output.png", "rb") as f:
                    st.download_button("Download", f, file_name="enhanced.png")

    # ---------- STRIPE ----------
    elif option == "Upgrade":

        st.write("Upgrade to Pro")

        if st.button("Pay $5"):
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Pro Plan"},
                        "unit_amount": 500,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://your-app.streamlit.app",
                cancel_url="https://your-app.streamlit.app",
            )

            st.markdown(f"[Pay Now]({session.url})")