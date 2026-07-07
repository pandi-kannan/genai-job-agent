import streamlit as st
from agent import app as agent_app
from tools import parse_resume_pdf
from db import init_db, save_analysis, get_all_analyses
import tempfile

st.set_page_config(page_title="Job Application Assistant", layout="wide")

try:
    init_db()
except Exception as e:
    st.warning("Database is waking up, please refresh in a few seconds.")

st.title("🎯 AI Job Application Assistant")
st.write("Upload your resume and paste a job description to get a tailored gap analysis and resume bullets.")

tab1, tab2 = st.tabs(["New Analysis", "History"])

with tab1:
    company_name = st.text_input("Company Name")
    job_description = st.text_area("Paste Job Description", height=200)
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if st.button("Run Analysis"):
        if not (company_name and job_description and resume_file):
            st.warning("Please fill in all fields and upload your resume.")
        else:
            with st.spinner("Agent is working..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(resume_file.read())
                    tmp_path = tmp.name

                resume_text = parse_resume_pdf(tmp_path)

                result = agent_app.invoke({
                    "job_description": job_description,
                    "resume_text": resume_text,
                    "company_name": company_name,
                    "job_summary": "",
                    "gaps": "",
                    "fit_score": "",
                    "company_info": "",
                    "bullets": ""
                })

                try:
                    save_analysis(
                        job_title=company_name,
                        company_name=company_name,
                        resume_gaps=result["gaps"],
                        suggested_bullets=result["bullets"]
                    )
                except Exception as e:
                    st.warning(f"Note: couldn't save to history ({e}), but here are your results anyway:")

            st.success("Analysis complete!")
            st.subheader("🎯 Fit Score")
            st.info(result["fit_score"])

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📋 Job Summary")
                st.write(result["job_summary"])

                st.subheader("🔍 Skill Gaps")
                st.write(result["gaps"])

            with col2:
                st.subheader("🏢 Company Info")
                st.write(result["company_info"])

                st.subheader("✍️ Suggested Resume Bullets")
                st.write(result["bullets"])

with tab2:
    st.subheader("Past Analyses")
    records = get_all_analyses()
    if not records:
        st.info("No past analyses yet.")
    for r in records:
        with st.expander(f"{r.company_name} — {r.created_at.strftime('%Y-%m-%d %H:%M')}"):
            st.write("**Gaps:**", r.resume_gaps)
            st.write("**Bullets:**", r.suggested_bullets)