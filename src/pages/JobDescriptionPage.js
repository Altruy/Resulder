import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const JobDescriptionPage = () => {
  const [jobDescription, setJobDescription] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  // Retrieve the resume path from the previous page
  const resumePath = location.state?.resumePath;

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('resume_path', resumePath);
    formData.append('job_description', jobDescription);

    const response = await fetch('http://127.0.0.1:8000/submit_job_description/', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      // Navigate to the Cover Letter Page and pass the generated cover letter
      navigate('/cover-letter', { state: { coverLetter: data.cover_letter } });
    } else {
      console.error('Failed to submit job description');
    }
  };

  return (
    <div>
      <h1>Enter Job Description</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={jobDescription}
          onChange={handleJobDescriptionChange}
          rows="10"
          cols="50"
          placeholder="Paste the job description here"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default JobDescriptionPage;
