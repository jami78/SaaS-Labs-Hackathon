# streamlit_app.py

import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # adjust if hosted elsewhere

st.title("🧠 Strategy Assistant UI")

tab1, tab2 = st.tabs(["📣 Content Agent", "💸 Pricing Agent"])

# -----------------------------
# 📣 TAB 1: Content Agent
# -----------------------------
with tab1:
    st.header("📣 Content Generation")
    user_input = st.text_area("Enter your product context or request:")

    pdf_file = st.file_uploader("Upload a reference PDF (optional)", type=["pdf"], key="content_pdf")

    if st.button("Run Content Agent", key="content_btn"):
        files = {}
        if pdf_file:
            files["pdf_file"] = (pdf_file.name, pdf_file, "application/pdf")

        response = requests.post(
            f"{API_BASE_URL}/content/",
            params={"input": user_input},
            files=files
        )

        if response.status_code == 200:
            st.success("✅ Content agent response:")
            st.write(response.json()["response"])
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.json(response.json())


# -----------------------------
# 💸 TAB 2: Pricing Agent
# -----------------------------
with tab2:
    st.header("💸 Pricing & Financial Strategy")

    user_input = st.text_area("Describe your pricing challenge or product setup:")

    pdf_file = st.file_uploader("Upload a reference PDF (optional)", type=["pdf"], key="pricing_pdf")
    excel_file = st.file_uploader("Upload financial data (.xlsx)", type=["xlsx"], key="pricing_excel")

    if st.button("Run Pricing Agent", key="pricing_btn"):
        files = {}
        if pdf_file:
            files["pdf_file"] = (pdf_file.name, pdf_file, "application/pdf")
        if excel_file:
            files["excel_file"] = (excel_file.name, excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response = requests.post(
            f"{API_BASE_URL}/pricing/",
            params={"input": user_input},
            files=files
        )

        if response.status_code == 200:
            st.success("✅ Pricing agent response:")
            st.write(response.json()["response"])
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.json(response.json())
