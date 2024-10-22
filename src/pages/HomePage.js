import React, { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Typography,
  Grid,
  CircularProgress,
  Box,
} from "@mui/material";
import { useForm } from "react-hook-form";
import axios from "axios";

const BACKEND_URL = "http://127.0.0.1:8000";

const ResumeUploader = () => {
  const [resumeDetail, setResumeDetail] = useState({});
  const [loading, setLoading] = useState(false);
  const [coverLetter, setCoverLetter] = useState(null);
  const [emailValid, setEmailValid] = useState(false);
  const [resumePath, setResumePath] = useState(null);

  // Added getValues here
  const { register, handleSubmit, getValues, formState: { errors }, reset } = useForm();

  // Retrieve resume details from backend
  const onSubmitEmail = async (data) => {
    setLoading(true);
    setEmailValid(false);
    try {
      const response = await axios.post(`${BACKEND_URL}/resume_details/`, {
        email: data.email,
      });
      setResumeDetail(response.data.profile);
      setResumePath(response.data.resume_path);
      setEmailValid(true);
      reset();
    } catch (error) {
      console.error("Error retrieving resume details:", error);
    } finally {
      setLoading(false);
    }
  };

  // Submit updated resume details
  const updateResume = async (updatedData) => {
    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/submit_resume_details/`, {
        ...updatedData,
        Email: resumeDetail.Email,
      });
      console.log(response.data);
      alert("Resume details saved successfully!");
    } catch (error) {
      console.error("Failed to update resume details", error);
    } finally {
      setLoading(false);
    }
  };

  // Generate Cover Letter
  const generateCoverLetter = async (jobDescription) => {
    if (!resumePath) return alert("Resume path not found!");

    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/generate_cover_letter/`, {
        resume_path: resumePath,
        job_description: jobDescription,
      });
      setCoverLetter(response.data.cover_letter);
    } catch (error) {
      console.error("Failed to generate cover letter", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ textAlign: "center", mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Resume and Job Description Uploader
      </Typography>

      {/* Step 1: Enter Email */}
      <Typography variant="h6" gutterBottom>
        Step 1: Enter Your Resume Details
      </Typography>
      <form onSubmit={handleSubmit(onSubmitEmail)}>
        <TextField
          label="Email"
          fullWidth
          margin="normal"
          {...register("email", { required: "Email is required" })}
          error={!!errors.email}
          helperText={errors.email ? errors.email.message : ""}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Retrieve Resume Details"}
        </Button>
      </form>

      {emailValid && (
        <>
          <Typography variant="h6" gutterBottom mt={4}>
            Update Your Profile Details
          </Typography>

          {/* Profile Details Form */}
          <form onSubmit={handleSubmit(updateResume)}>
            <TextField
              label="About Me"
              multiline
              rows={4}
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.AboutMe}
              {...register("AboutMe")}
            />
            <TextField
              label="Contact"
              multiline
              rows={2}
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Contact}
              {...register("Contact")}
            />
            <TextField
              label="Education"
              multiline
              rows={4}
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Education}
              {...register("Education")}
            />
            <TextField
              label="Experience"
              multiline
              rows={6}
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Experience}
              {...register("Experience")}
            />
            <TextField
              label="Expertise"
              multiline
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Expertise}
              {...register("Expertise")}
            />
            <TextField
              label="Skills"
              multiline
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Skills}
              {...register("Skills")}
            />
            <TextField
              label="Languages"
              multiline
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Languages}
              {...register("Languages")}
            />
            <TextField
              label="Research"
              multiline
              fullWidth
              margin="normal"
              defaultValue={resumeDetail.Research}
              {...register("Research")}
            />

            <Button
              type="submit"
              variant="contained"
              color="secondary"
              fullWidth
              sx={{ mt: 3 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : "Update Resume"}
            </Button>
          </form>
        </>
      )}

      {/* Step 2: Job Description */}
      {emailValid && (
        <>
          <Typography variant="h6" gutterBottom mt={4}>
            Step 2: Enter Job Description
          </Typography>
          <TextField
            label="Paste the Job Description here"
            multiline
            rows={6}
            fullWidth
            margin="normal"
            variant="outlined"
            {...register("jobDescription")}
          />
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 3 }}
            onClick={() => generateCoverLetter(getValues("jobDescription"))}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : "Generate Cover Letter"}
          </Button>
        </>
      )}

      {coverLetter && (
        <Box mt={4}>
          <Typography variant="h6">Generated Cover Letter</Typography>
          <TextField
            multiline
            rows={10}
            fullWidth
            margin="normal"
            variant="outlined"
            value={coverLetter}
            readOnly
          />
          <Button
            variant="contained"
            color="secondary"
            fullWidth
            sx={{ mt: 3 }}
            onClick={() => {
              const blob = new Blob([coverLetter], { type: "text/plain" });
              const link = document.createElement("a");
              link.href = URL.createObjectURL(blob);
              link.download = "cover_letter.txt";
              link.click();
            }}
          >
            Download Cover Letter
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default ResumeUploader;
