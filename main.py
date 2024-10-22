from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from fpdf import FPDF
from openai import OpenAI
import hashlib



app = FastAPI()

# Set up OpenAI API key
client = OpenAI(api_key="")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExtraField(BaseModel):
    field: str
    value: str

class ResumeData(BaseModel):
    AboutMe: str  = None
    Contact: str  = None
    Education: str  = None
    Email: str  = None
    Experience: str  = None
    Expertise: str  = None
    Languages: str  = None
    Skills: str  = None
    Research: str = None
    extraFields: Optional[List[ExtraField]] = None

class JobDescription(BaseModel):
    description: str

class CoverLetterRequest(BaseModel):
    email: str = None
    job_description : str = None
    resume_path : str = None

@app.post("/resume_details")
async def get_resume_details(request: CoverLetterRequest):
    # Save resume data as JSON
    email = request.email
    resume_path = f"./resumes/{email}.json"
    try:
        with open(resume_path, 'r') as f:
            profile = json.load(f)

        return {"profile" : profile, "resume_path": resume_path}
    except : return {"profile" : {"About Me": "","Contact": "","Education": "","Experience": "","Expertise": "","Skills": "","Languages": "","Research": "","Extra Fields": {}}, "resume_path":None}

@app.post("/submit_resume_details")
async def submit_resume(resume_data: ResumeData):
    print(resume_data)
    profile_data = {
        "AboutMe": resume_data.AboutMe,
        "Contact": resume_data.Contact,
        "Education": resume_data.Education,
        "Experience": resume_data.Experience,
        "Expertise": resume_data.Expertise,
        "Skills": resume_data.Skills,
        "Languages": resume_data.Languages,
        "Research": resume_data.Research,
        "Extra Fields": {field.field: field.value for field in resume_data.extraFields} if resume_data.extraFields else {}
    }
    
    # Save resume data as JSON
    email = resume_data.Email
    file_path = f"./resumes/{email}.json"
    os.makedirs("./resumes", exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(profile_data, f)
    
    return {"message": "Resume saved successfully","resume_path":file_path}

@app.post("/generate_cover_letter")
async def generate_cover_letter(request: CoverLetterRequest):
    resume_path = request.resume_path
    job_description = request.job_description
    
    # Read the resume file
    if not os.path.exists(resume_path):
        return {"error": "Resume not found"}
    
    with open(resume_path, 'r') as f:
        profile = json.load(f)
    
    # save job description
    file_path = "./job_descriptions/job_description.txt"
    os.makedirs("./job_descriptions", exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(job_description)
    
    # Generate cover letter using OpenAI
    prompt = f"Create a professional cover email letter based on the following profile: {profile} and job description: {job_description}."
    prompt_hash = hashlib.sha1(prompt.encode()).hexdigest()
    with open('hash_letters.json', 'r') as f:
        cover_letter_hashed = json.load(f)
    if prompt_hash in cover_letter_hashed:
        return {"cover_letter": cover_letter_hashed.get(prompt_hash)}
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    cover_letter = response.choices[0].message.content
    cover_letter_hashed[prompt_hash] = cover_letter

    with open('hash_letters.json', 'w') as f:
        json.dump(cover_letter_hashed, f)


    # save job description
    file_path = "./cover_letter/cover_letter.txt"
    os.makedirs("./cover_letter", exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(cover_letter)
    
    return {"cover_letter": cover_letter}

@app.post("/download_cover_letter")
async def download_cover_letter(request: Request):
    data = await request.json()
    cover_letter = data.get('cover_letter', '')
    
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=cover_letter)
    
    # Save PDF file
    pdf_file_path = "./cover_letters/cover_letter.pdf"
    os.makedirs("./cover_letters", exist_ok=True)
    pdf.output(pdf_file_path)
    
    return FileResponse(pdf_file_path, media_type='application/pdf', filename='cover_letter.pdf')
