// src/components/SalaryPredictionForm.js
import React, { useState } from 'react';

const SalaryPredictionForm = ({ data }) => {
  const [formData, setFormData] = useState({
    job_title: '',
    experience_level: '',
    location: '',
    work_setting: '',
  });
  const [predictedSalary, setPredictedSalary] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const predictSalary = () => {
    // Simple average calculation based on filters
    const filteredData = data.filter(
      (item) =>
        item.job_title === formData.job_title &&
        item.experience_level === formData.experience_level &&
        item.location === formData.location &&
        item.work_setting === formData.work_setting
    );

    if (filteredData.length > 0) {
      const averageSalary =
        filteredData.reduce((sum, item) => sum + parseFloat(item.salary), 0) /
        filteredData.length;
      setPredictedSalary(averageSalary.toFixed(2));
    } else {
      setPredictedSalary('No data available for the selected criteria.');
    }
  };

  return (
    <div>
      <h3>Salary Prediction</h3>
      <input
        type="text"
        name="job_title"
        placeholder="Job Title"
        onChange={handleChange}
      />
      <input
        type="text"
        name="experience_level"
        placeholder="Experience Level"
        onChange={handleChange}
      />
      <input
        type="text"
        name="location"
        placeholder="Location"
        onChange={handleChange}
      />
      <input
        type="text"
        name="work_setting"
        placeholder="Work Setting"
        onChange={handleChange}
      />
      <button onClick={predictSalary}>Predict Salary</button>
      {predictedSalary && <p>Predicted Salary: {predictedSalary}</p>}
    </div>
  );
};

export default SalaryPredictionForm;
