import streamlit as st

st.set_page_config(
    page_title="Supercar Intelligence Hub",
    page_icon="🏎️",
    layout="wide"
)

# --- Sidebar navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Chatbot"])

# --- Home Page ---
if page == "Home":
    st.title("🏠 Welcome to the Supercar Project")

    st.markdown("""
    ## 🚀 Project Overview

    This project focuses on **Supercars**, including:

    ### 🔹 1. Live Data Collection  
    Real-time scraping from supercar listing sites such as AutoTrader UK, PistonHeads, Cars.com, and more.

    ### 🔹 2. Data Cleaning & Storage  
    Standardizing car names, prices, and saving cleaned data.

    ### 🔹 3. Dashboard in Power BI  
    Interactive visuals on price trends, brand comparisons, mileage effects, and depreciation.

    ### 🔹 4. Car Price Prediction (ML Model)  
    Using models like Random Forest, XGBoost, and Linear Regression for price forecasting.

    ### 🔹 5. Chatbot  
    An AI assistant answering supercar-related questions.

    ---
    Use the sidebar to switch between pages and explore the app.
    """)

# --- Chatbot Page ---
elif page == "Chatbot":
    st.title("💬 Supercar Chatbot")

    st.write("Ask me anything about supercars!")

    def simple_chatbot(user_input):
        user_input = user_input.lower()

        if "ferrari" in user_input:
            return "Ferrari is famous for its V8 and V12 engines. The 488, F8 and SF90 are top models."
        if "lamborghini" in user_input:
            return "Lamborghini is known for aggressive designs. Popular models include the Huracan and Aventador."
        if "porsche" in user_input:
            return "Porsche is performance-focused. The 911 Turbo S and GT3 are iconic supercars."
        if "mclaren" in user_input:
            return "McLaren supercars include the 720S, Artura and the hybrid P1."
        if "price" in user_input:
            return "Supercar prices vary widely depending on mileage, spec, and year. More analytics coming soon."
        if "hello" in user_input or "hi" in user_input:
            return "Hello! What supercar do you want to talk about?"
        if "buy" in user_input:
            return "Buying a supercar? Look for condition, service history, mileage and depreciation trends."

        return "I am still learning! Ask me about Ferrari, Lamborghini, Porsche, McLaren or supercar prices."

    user_message = st.text_input("Your Question:")

    if user_message:
        bot_response = simple_chatbot(user_message)
        st.markdown(f"**Bot:** {bot_response}")
