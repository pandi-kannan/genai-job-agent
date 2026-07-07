import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict
from tools import search_company_info

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

class AgentState(TypedDict):
    job_description: str
    resume_text: str
    company_name: str
    job_summary: str
    gaps: str
    company_info: str
    bullets: str
    fit_score: str

def fit_score_node(state: AgentState):
    prompt = f"""Based on the job requirements and identified gaps below, give a Fit Score 
    from 0-100 representing how well this candidate matches the job, followed by a one-line label.

    Respond in EXACTLY this format, nothing else:
    Score: <number>
    Label: <Strong Match / Good Match / Moderate Match / Weak Match>
    Reason: <one sentence explaining the score>

    JOB REQUIREMENTS:
    {state['job_summary']}

    IDENTIFIED GAPS:
    {state['gaps']}

    RESUME:
    {state['resume_text']}"""
    response = llm.invoke(prompt)
    state["fit_score"] = response.content
    return state

def summarize_job_node(state: AgentState):
    prompt = f"""Summarize this job description in 3-4 bullet points, 
    focusing on key required skills and responsibilities:

    {state['job_description']}"""
    response = llm.invoke(prompt)
    state["job_summary"] = response.content
    return state

def gap_analysis_node(state: AgentState):
    prompt = f"""Compare this resume against the job requirements below.
    List the top 3-5 skill or experience gaps as bullet points.

    JOB REQUIREMENTS:
    {state['job_summary']}

    RESUME:
    {state['resume_text']}"""
    response = llm.invoke(prompt)
    state["gaps"] = response.content
    return state

def company_search_node(state: AgentState):
    state["company_info"] = search_company_info(state["company_name"])
    return state

def bullet_generator_node(state: AgentState):
    prompt = f"""Based on the resume, job requirements, and identified gaps below, 
    write 3 tailored, quantified resume bullet points that better align this candidate 
    with the job. Keep them honest and realistic based on their actual resume content.

    JOB REQUIREMENTS:
    {state['job_summary']}

    IDENTIFIED GAPS:
    {state['gaps']}

    CURRENT RESUME:
    {state['resume_text']}"""
    response = llm.invoke(prompt)
    state["bullets"] = response.content
    return state

graph = StateGraph(AgentState)
graph.add_node("summarize_job", summarize_job_node)
graph.add_node("gap_analysis", gap_analysis_node)
graph.add_node("fit_score", fit_score_node)
graph.add_node("company_search", company_search_node)
graph.add_node("bullet_generator", bullet_generator_node)

graph.set_entry_point("summarize_job")
graph.add_edge("summarize_job", "gap_analysis")
graph.add_edge("gap_analysis", "fit_score")
graph.add_edge("fit_score", "company_search")
graph.add_edge("company_search", "bullet_generator")
graph.add_edge("bullet_generator", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({
        "job_description": "We are looking for a GenAI Developer with experience in LangChain, RAG systems, Python, and vector databases like ChromaDB.",
        "resume_text": "B.Tech IT graduate with Java Spring Boot experience, built a RAG PDF chatbot using LangChain and ChromaDB.",
        "company_name": "OpenAI",
        "job_summary": "",
        "gaps": "",
        "fit_score": "",
        "company_info": "",
        "bullets": ""
    })
    print("FIT SCORE:\n", result["fit_score"])
    print("\nJOB SUMMARY:\n", result["job_summary"])
    print("\nGAPS:\n", result["gaps"])
    print("\nCOMPANY INFO:\n", result["company_info"])
    print("\nBULLETS:\n", result["bullets"])