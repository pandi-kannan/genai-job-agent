import pdfplumber
from ddgs import DDGS
def parse_resume_pdf(file_path: str) -> str:
    """Extracts text from an uploaded resume PDF."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def search_company_info(company_name: str) -> str:
    """Searches the web for basic company info."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{company_name} company overview", max_results=3))
        summary = "\n".join([r.get("body", "") for r in results])
        return summary if summary else "No company info found."
    except Exception as e:
        return f"Search failed: {str(e)}"