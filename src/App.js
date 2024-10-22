import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import JobDescriptionPage from './pages/JobDescriptionPage';
import CoverLetterPage from './pages/CoverLetterPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/job-description" element={<JobDescriptionPage />} />
        <Route path="/cover-letter" element={<CoverLetterPage />} />
      </Routes>
    </Router>
  );
}

export default App;
