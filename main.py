from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import openai
import docx
import os
import pdfkit
from typing import List, Dict

app = FastAPI()

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simulate a database
database = {}

# Pydantic models for request body
class JobDescription(BaseModel):
    description: str

# Utility function to parse the resume DOCX
def parse_resume(file: UploadFile):
    doc = docx.Document(file.file)
    profile_data = {}
    current_heading = None
    
    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            current_heading = para.text
            profile_data[current_heading] = []
        elif current_heading:
            profile_data[current_heading].append(para.text)

    return profile_data

# Endpoint to upload the resume and parse it
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    profile_data = parse_resume(file)
    database['profile'] = profile_data
    return {"message": "Resume uploaded and parsed successfully", "profile": profile_data}

# Endpoint to modify Experience, Skills, and Expertise using LLM based on job description
@app.post("/modify_resume/")
async def modify_resume(job: JobDescription):
    profile = database.get('profile')
    
    if not profile:
        return {"error": "Resume not found"}

    experience_text = "\n".join(profile.get("Experience", []))
    skills_text = "\n".join(profile.get("Skills", []))
    expertise_text = "\n".join(profile.get("Expertise", []))

    prompt = f"""
    I have the following job description: {job.description}

    My current experience is: {experience_text}
    My current skills are: {skills_text}
    My current expertise is: {expertise_text}

    Can you modify them to best fit the job description?
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
    )

    modified_resume = response.choices[0].text.strip()
    
    # Save the modified resume to the database
    database['modified_resume'] = modified_resume

    return {"modified_resume": modified_resume}

# Endpoint to generate the cover letter
@app.post("/generate_cover_letter/")
async def generate_cover_letter(job: JobDescription):
    profile = database.get('profile')

    if not profile:
        return {"error": "Resume not found"}

    about_me_text = "\n".join(profile.get("About Me", []))

    prompt = f"""
    I have the following job description: {job.description}

    My introduction (About Me) is: {about_me_text}

    Can you generate a professional cover letter for this job?
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
    )

    cover_letter = response.choices[0].text.strip()

    return {"cover_letter": cover_letter}

# Endpoint to download the modified resume as a PDF
@app.get("/download_resume/")
async def download_resume():
    modified_resume = database.get('modified_resume')

    if not modified_resume:
        return {"error": "Modified resume not found"}

    # Use PDFKit to generate PDF from modified_resume text
    pdf_path = "/tmp/modified_resume.pdf"
    pdfkit.from_string(modified_resume, pdf_path)

    return {"pdf_path": pdf_path}
