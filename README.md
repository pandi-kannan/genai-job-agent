# 🎯 AI Job Application Assistant

An autonomous AI agent that helps job seekers tailor their resumes to specific job postings — analyzing skill gaps, researching companies, and generating quantified resume bullet points, all through a multi-step LangGraph agent pipeline.

## 📌 Problem Statement

Job seekers, especially freshers, spend significant time manually comparing their resume against job descriptions, researching companies, and rewriting bullet points for every application. This project automates that workflow using an AI agent that reasons through the process step by step, rather than relying on a single prompt.

## ✨ Features

- **Job Description Summarization** — extracts key requirements and responsibilities from any job posting
- **Resume Gap Analysis** — compares your resume against the job requirements and identifies specific skill/experience gaps
- **Live Company Research** — pulls up-to-date company information via web search
- **AI-Generated Resume Bullets** — produces tailored, quantified bullet points grounded in your actual resume content
- **Application History** — every analysis is saved to a PostgreSQL database, so you can track past applications and revisit tailored suggestions

## 🏗️ Architecture

The core of this project is an **agent graph** built with LangGraph, where each step is an independent node that passes shared state forward: