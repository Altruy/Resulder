import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Streamlit UI for resume upload or manual input
st.title("Resume and Job Description Uploader")

# Step 1: Choose between uploading resume or entering details manually
st.header("Step 1: Enter Your Resume details")

if "resume_path" not in st.session_state:
    st.session_state.resume_path = None
if "email_valid" not in st.session_state:
    st.session_state.email_valid = False
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = None
class ResumeData:
    AboutMe: str
    Contact: str
    Education: str
    Email: str
    Experience: str
    Expertise: str
    Languages: str
    Skills: str
    Research: str

resume_detail = {}
st.session_state.email = st.text_input("Email")
if st.button("Retrieve Resume Details"):
    if not st.session_state.email:
        st.session_state.email_valid = False
        st.error("Please enter a email")
    else:
        # Send resume path and job description to the backend
        st.session_state.email_valid = True
        with st.spinner('Retrieving Profile...'):
            form_data = {
                'email': st.session_state.email
            }
            response = requests.post(f"{BACKEND_URL}/resume_details/", data=json.dumps(form_data))

            if response.status_code == 200:
                data = response.json()
                resume_detail["AboutMe"] = data.get('profile').get('AboutMe')
                resume_detail["Contact"] = data.get('profile').get("Contact")
                resume_detail["Education"] = data.get('profile').get("Education")
                resume_detail["Experience"] = data.get('profile').get("Experience")
                resume_detail["Expertise"] = data.get('profile').get("Expertise")
                resume_detail["Skills"] = data.get('profile').get("Skills")
                resume_detail["Languages"] = data.get('profile').get("Languages")
                resume_detail["Research"] = data.get('profile').get("Research")
                st.session_state.resume_path = data.get('resume_path')  
                st.session_state.email_valid = True                              

if st.session_state.email_valid:
    st.subheader("Update your profile details")
    st.session_state.AboutMe = st.text_area("About Me", value=st.session_state.AboutMe)
    st.session_state.Contact = st.text_area("Contact Information", value=st.session_state.Contact)
    st.session_state.Education = st.text_area("Education", value=st.session_state.Education)
    st.session_state.Experience = st.text_area("Experience", value=st.session_state.Experience, height=600)
    st.session_state.Expertise = st.text_area("Expertise", value=st.session_state.Expertise)
    st.session_state.Skills = st.text_area("Skills", value=st.session_state.Skills)
    st.session_state.Languages = st.text_area("Languages", value=st.session_state.Languages)
    st.session_state.Research = st.text_area("Research", value=st.session_state.Research)

    if st.button("Update Resume"):
        with st.spinner('Submitting resume details...'):
            resume_data = {
            "Email" : st.session_state.email,
            "AboutMe" : st.session_state.AboutMe,
            "Contact" : st.session_state.Contact,
            "Education" : st.session_state.Education,
            "Experience" : st.session_state.Experience,
            "Expertise" : st.session_state.Expertise,
            "Skills" : st.session_state.Skills,
            "Languages" : st.session_state.Languages,
            "Research" : st.session_state.Research,
            }
            response = requests.post(f"{BACKEND_URL}/submit_resume_details/", json=resume_data)

            if response.status_code == 200:
                data = response.json()
                st.success("Resume details saved successfully!")
            else:
                st.error("Failed to save the resume details.")


# Step 2: Enter Job Description
if st.session_state.resume_path and st.session_state.email_valid:
    st.header("Step 2: Enter Job Description")
    job_description = st.text_area("Paste the job description here",height=300)

    if st.button("Generate Cover Letter"):
        if not job_description:
            st.error("Please enter a job description.")
        else:
            # Send resume path and job description to the backend
            with st.spinner('Generating cover letter...'):
                form_data = {
                    'resume_path': st.session_state.resume_path,
                    'job_description': job_description
                }
                response = requests.post(f"{BACKEND_URL}/generate_cover_letter/", data=json.dumps(form_data))

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.cover_letter = data.get("cover_letter")
                    st.success("Cover letter generated successfully!")
                    
                    # Display the generated cover letter
                    st.header("Generated Cover Letter")
                    st.text_area("Generated Cover Letter", value=st.session_state.cover_letter, height=500)
                    
                    # Option to download the cover letter as a text file
                    st.download_button(
                        label="Download Cover Letter",
                        data=st.session_state.cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Failed to generate cover letter.")