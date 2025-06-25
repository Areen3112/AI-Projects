import os
import fitz  # PyMuPDF
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyD_Ty7IdnLfaz0w1XiWVp1NFXonA4H2oKs"))

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyze_resume(jd, resume_text):
    prompt = f"""
You are a professional resume reviewer.

Here is the job description:
{jd}

Here is the resume:
{resume_text}

Please provide:
1. A resume fit score out of 100.
2. Top 5 strengths.
3. Top 5 weaknesses or missing skills.
4. Suggestions to improve the resume.
5. Recommended courses or YouTube videos to bridge the gap.
    """

    try:
        # ✅ Use correct model name from your available list
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text or "❌ No response received from Gemini."
    except Exception as e:
        print("❌ Gemini Error:", e)
        return f"❌ Error occurred: {e}"
