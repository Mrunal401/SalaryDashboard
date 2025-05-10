
import React, { useEffect, useState } from "react";
import axios from "axios";
import FilterPanel from "./components/FilterPanel";
import SalaryChart from "./components/SalaryChart";

const App = () => {
  const [filters, setFilters] = useState({ job_title: "", job_category: "", location: "" });
  const [options, setOptions] = useState({ job_titles: [], job_categories: [], locations: [] });
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/filters").then(res => setOptions(res.data));
  }, []);

  useEffect(() => {
    axios.post("http://localhost:5000/api/salary-summary", filters)
         .then(res => setChartData(res.data));
  }, [filters]);

  return (
    <div className="App">
      <h1>Salary Analysis Dashboard</h1>
      <FilterPanel filters={filters} setFilters={setFilters} options={options} />
      <SalaryChart data={chartData} />
    </div>
  );
};

export default App;
