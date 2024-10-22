# Resume and Cover Letter Generator

This project is a **Resume and Cover Letter Generator** application that allows users to either upload their resume or manually enter details, generate cover letters tailored to specific job descriptions, and download them in various formats. It is powered by a **FastAPI** backend and has two frontend options: **Streamlit** and **React**.

## Features

1. **Resume Upload/Entry**: Users can either upload their resume or manually input details like education, experience, skills, and contact information.
2. **Job Description Input**: Users can enter a job description to tailor the cover letter accordingly.
3. **Cover Letter Generation**: The backend uses OpenAI's GPT model to generate a professional cover letter based on the resume details and job description.
4. **Download**: Users can download the generated cover letter in text or PDF format.
5. **Two Frontend Options**:
   - **Streamlit** for quick prototyping and a simple UI.
   - **React** for a more modern and scalable front-end application.

## Tech Stack

- **Backend**: FastAPI, OpenAI API, FPDF
- **Frontend**: 
  - **Streamlit**: Simple web interface for interacting with the backend.
  - **React**: An alternative frontend for a more scalable and interactive user interface.
- **Database**: JSON-based storage for resumes and job descriptions (can be extended to a database like PostgreSQL or MongoDB).
- **Deployment**: The backend serves static files and handles API requests for generating cover letters and managing resumes.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js (for React frontend)
- OpenAI API key

### Backend Setup (FastAPI)

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/resume-cover-letter-generator.git
    cd resume-cover-letter-generator
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set your OpenAI API key in the FastAPI app by replacing the placeholder in the `client = OpenAI(api_key="")` line with your API key.

5. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

6. The backend will be running at `http://127.0.0.1:8000`.

### Streamlit Frontend Setup

1. Install Streamlit:

    ```bash
    pip install streamlit
    ```

2. Run the Streamlit app:

    ```bash
    streamlit run streamlit_app.py
    ```

3. Access the app at `http://localhost:8501`.

### React Frontend Setup (Optional)

1. Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the React app:

    ```bash
    npm start
    ```

4. Access the React frontend at `http://localhost:3000`.

## API Endpoints

### Resume Management

- **POST /resume_details**: Retrieve resume details based on email.
- **POST /submit_resume_details**: Save or update resume details in the backend.

### Cover Letter Generation

- **POST /generate_cover_letter**: Generate a cover letter based on the resume and job description.
- **POST /download_cover_letter**: Generate and download the cover letter as a PDF.

## How to Use

1. **Step 1: Enter Resume Details**
   - Upload your resume or manually enter the details like experience, education, and skills.
   
2. **Step 2: Enter Job Description**
   - Paste the job description of the role you're applying for.

3. **Step 3: Generate and Download Cover Letter**
   - Click the "Generate Cover Letter" button. Once generated, download it as a text file or PDF.

## Customization

- Modify the OpenAI model prompt in the `/generate_cover_letter` API route to customize the tone or content of the generated cover letter.
- The application currently uses JSON to store resumes and job descriptions. You can replace this with a database for scalability.

## Future Enhancements

- Integrate a database like MongoDB or PostgreSQL for persistent storage.
- Add user authentication for secure resume storage and management.
- Implement job-matching algorithms to recommend job descriptions.

## License

This project is licensed under the MIT License.
