import React from 'react';
import { useLocation } from 'react-router-dom';

const CoverLetterPage = () => {
  const location = useLocation();
  const coverLetter = location.state?.coverLetter;

  return (
    <div>
      <h1>Generated Cover Letter</h1>
      <div>
        <h2>Cover Letter:</h2>
        <p>{coverLetter}</p>
      </div>
    </div>
  );
};

export default CoverLetterPage;
