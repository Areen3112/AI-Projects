import streamlit as st
from utils import extract_text_from_pdf, analyze_resume
import os

st.set_page_config(page_title="Resume Ranker", layout="centered")
st.title("📄 Resume Ranker & Career Coach")
st.write("Upload your resume and paste a job description. Get an AI-powered resume score and improvement tips!")

jd = st.text_area("Paste Job Description:", height=200)

uploaded_file = st.file_uploader("Upload Resume (PDF only):", type=["pdf"])

if uploaded_file and jd:
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        feedback = analyze_resume(jd, resume_text)

    st.success("Analysis Complete ✅")
    st.markdown("### 📊 Result")
    st.markdown(feedback)
