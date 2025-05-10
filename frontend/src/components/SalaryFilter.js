import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import {
  Box, Button, Card, CardActions, CardContent, MenuItem, Select, Typography,
  FormControl, InputLabel, Paper, TextField, Divider
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#1e88e5' },
    secondary: { main: '#f50057' },
  },
  shape: {
    borderRadius: 12,
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

const SalaryFilter = () => {
  const [categories, setCategories] = useState([]);
  const [titles, setTitles] = useState([]);
  const [locations, setLocations] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedTitle, setSelectedTitle] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [averageSalary, setAverageSalary] = useState(null);
  const [salaryByExp, setSalaryByExp] = useState([]);

  const [experience, setExperience] = useState('');
  const [userSalary, setUserSalary] = useState('');
  const [showAnalysis, setShowAnalysis] = useState(false);

  const [salaryCheckResult, setSalaryCheckResult] = useState(null);
  const experienceLevels = ['Entry-level', 'Mid-level', 'Senior', 'Executive'];



  const API_BASE = 'http://127.0.0.1:5000'; // Flask URL

  useEffect(() => {
    fetch(`${API_BASE}/categories`)
      .then(res => res.json())
      .then(data => setCategories(data));
  }, []);

  const handleCategoryChange = (e) => {
    const category = e.target.value;
    setSelectedCategory(category);
    setSelectedTitle('');
    setSelectedLocation('');
    setAverageSalary(null);
    setSalaryByExp([]);
    setSalaryCheckResult(null);

    fetch(`${API_BASE}/titles?category=${category}`)
      .then(res => res.json())
      .then(data => setTitles(data));
  };

  const handleTitleChange = (e) => {
    const title = e.target.value;
    setSelectedTitle(title);
    setSelectedLocation('');
    setAverageSalary(null);
    setSalaryByExp([]);
  setSalaryCheckResult(null);

    fetch(`${API_BASE}/locations?category=${selectedCategory}&title=${title}`)
      .then(res => res.json())
      .then(data => setLocations(data));
  };

  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
  };
  
  const fetchSalaryData = () => {
    if (selectedCategory && selectedTitle && selectedLocation) {
      fetch(`${API_BASE}/average_salary?category=${selectedCategory}&title=${selectedTitle}&location=${selectedLocation}`)
        .then(res => res.json())
        .then(data => {
          if (data && data.average_salary) {
            setAverageSalary(data.average_salary);
          } else {
            setAverageSalary(null);
          }
        })
        .catch(err => console.error("Error fetching average salary:", err));
  
        //.then(data => setAverageSalary(data.average_salary));
  
      fetch(`${API_BASE}/salary_by_experience?category=${selectedCategory}&title=${selectedTitle}&location=${selectedLocation}`)
        .then(res => res.json())
        .then(data => setSalaryByExp(data));
      
    }
  };
  

return (
  <Box display="flex" flexDirection="column" alignItems="center" padding="20px">
    {/* <Typography variant="h6" gutterBottom align="center">
      Filter salary by job category, title, and location to get salary insights and trends.
    </Typography> */}

<Card
  sx={{
    width: '100%',
    maxWidth: 1000,
    mb: 4,
    boxShadow: 4,
    borderRadius: 3,
    background: '#f9f9fb'
  }}
>
  <CardContent>
    <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, textAlign: 'center' }}>
      Salary Calculator
    </Typography>
    <Typography variant="body1" color="text.secondary" align="center">
      Filter by job role, location, and experience to explore salary trends.
    </Typography>
  </CardContent>
</Card>

    {/* Input Section */}
    <Card sx={{ width: 1000, marginBottom: 4 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-around" flexWrap="wrap" gap={2}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Job Category</InputLabel>
            <Select value={selectedCategory} onChange={handleCategoryChange} label="Job Category">
              {categories.map((cat, idx) => (
                <MenuItem key={idx} value={cat}>{cat}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }} disabled={!selectedCategory}>
            <InputLabel>Job Title</InputLabel>
            <Select value={selectedTitle} onChange={handleTitleChange} label="Job Title">
              {titles.map((title, idx) => (
                <MenuItem key={idx} value={title}>{title}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }} disabled={!selectedTitle}>
            <InputLabel>Location</InputLabel>
            <Select value={selectedLocation} onChange={handleLocationChange} label="Location">
              {locations.map((loc, idx) => (
                <MenuItem key={idx} value={loc}>{loc}</MenuItem>
              ))}
            </Select>
          </FormControl>

        
          <Button
    variant="contained"
    size="large"
    color="primary"
    onClick={() => {
      fetchSalaryData();
      setShowAnalysis(true);
    }}
    sx={{
      height: 56,
      minWidth: 200,
      background: 'linear-gradient(to right, #8e24aa, #ec407a)',
      color: 'white',
      fontWeight: 600,
      boxShadow: 3,
      '&:hover': {
        background: 'linear-gradient(to right, #6a1b9a, #d81b60)',
        boxShadow: 4,
      }
    }}
  >
    Show Salary Insights
  </Button>
        </Box>
      </CardContent>
    </Card>

    {/* Salary Display Section */}
    {averageSalary && (
      <Card sx={{ width: 1000, marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" align="center">
            Average Salary: ${averageSalary.toLocaleString()}
          </Typography>
        </CardContent>
      </Card>
    )}

    {/* Salary by Experience Chart */}
    {salaryByExp.length > 0 && (
      <Card 
      sx={{
        width: '100%',
        maxWidth: 1000,
        height: 420,
        mb: 4,
        borderRadius: 3,
        boxShadow: 3,
        background: '#ffffff'
      }}
      //sx={{ width: 1000, height: 400 }}
      >
        <CardContent>
          <Typography variant="h6" align="center" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
            Average Salary by Experience Level
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salaryByExp}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="experience_level" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="salary_in_usd" fill="#42a5f5" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    )}

    {/* Personalized Salary Check Section */}
<Card sx={{ width: 1000, marginBottom: 4 }}>
  <CardContent>
  <Divider sx={{ width: '100%', my: 4 }} />
<Typography variant="h4" align="center" gutterBottom>
  Want to see how your salary compares?
</Typography>
    <Typography variant="h6" gutterBottom align="center">
      Personalized Salary Recommendation
    </Typography>

    {showAnalysis && (
  <Box display="flex" gap={2} mt={4} width="100%" justifyContent="center" flexWrap="wrap">
    <FormControl sx={{ minWidth: 200 }}>
      <InputLabel>Experience Level</InputLabel>
      <Select value={experience} onChange={(e) => setExperience(e.target.value)} label="Experience Level">
        {experienceLevels.map((level, idx) => (
          <MenuItem key={idx} value={level}>{level}</MenuItem>
        ))}
      </Select>
    </FormControl>


<FormControl sx={{ minWidth: 200 }}>
  <InputLabel shrink>User Salary (USD)</InputLabel>
  <TextField
  type="number"
  label="Your Salary (USD)"
  variant="outlined"
  fullWidth
  value={userSalary}
  onChange={(e) => setUserSalary(e.target.value)}
  sx={{ minWidth: 200 }}
/>

</FormControl>

<Button
  variant="contained"
  disabled={!experience || !userSalary || !salaryByExp.length}
  onClick={() => {
    const matching = salaryByExp.find(item => item.experience_level === experience);
    if (matching) {
      const diff = userSalary - matching.salary_in_usd;
      setSalaryCheckResult({
        target: matching.salary_in_usd,
        diff: diff.toFixed(2),
        higher: diff > 0
      });
    } else {
      setSalaryCheckResult({ noMatch: true });
    }
    setShowAnalysis(true);
  }}
  sx={{
    height: 56,
    minWidth: 200,
    background: 'linear-gradient(to right, #8e24aa, #ec407a)',
    color: 'white',
    fontWeight: 600,
    boxShadow: 3,
    '&:hover': {
      background: 'linear-gradient(to right, #6a1b9a, #d81b60)',
      boxShadow: 4,
    }
  }}

>
  Analyze My Salary
</Button>



  </Box>
)}

{showAnalysis && salaryCheckResult && (
  salaryCheckResult.noMatch ? (
    
    <Card 
    sx={{
      mt: 4,
      p: 4,
      maxWidth: 600,
      mx: 'auto',
      textAlign: 'center',
      backgroundColor: '#f5f5f5',
      boxShadow: 4,
      borderRadius: 3
    }}
    //sx={{ width: 600, mt: 4, padding: 3, backgroundColor: '#f9f9f9' }}
    >
    <Typography mt={2} color="error" fontWeight="bold">
      No records for this particular experience level.
    </Typography>
    </Card>
  ) : (
    <Card 
    sx={{ 
      mt: 4, 
      p: 3, 
      maxWidth: 600, 
      mx: 'auto', 
      backgroundColor: '#f9f9f9', 
      boxShadow: 3, 
      borderRadius: 3 
    }}
    //sx={{ width: 600, mt: 4, padding: 3, backgroundColor: '#f9f9f9' }}
    >
    <Paper elevation={3} style={{ padding: 20, marginTop: 20, maxWidth: 600 }}>
      <Typography variant="h6">Salary Comparison</Typography>
      <Typography>
        Average salary for {experience} professionals in this role/location: <strong>${salaryCheckResult.target}</strong>
      </Typography>
      <Typography color={salaryCheckResult.higher ? "green" : "red"}>
        Your salary is {salaryCheckResult.higher ? 'above' : 'below'} the average by ${Math.abs(salaryCheckResult.diff)}
      </Typography>
    </Paper>
    </Card>
  )
  
)}


  </CardContent>
</Card>

  </Box>
);

};

export default SalaryFilter;
