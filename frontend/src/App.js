import { useState } from 'react';
import './App.css';
import {
  AppBar, Box, Tab, Tabs, Toolbar, Typography, Container, Paper
} from "@mui/material";
import DashBoard from './components/DashBoard';
import Predictions from './components/Predictions';
import SalaryCalculator from './components/SalaryFilter';

function App() {
  const [currentTabIndex, setCurrentTabIndex] = useState(0);

  const handleTabChange = (e, tabIndex) => {
    setCurrentTabIndex(tabIndex);
  };

  return (
    <Box className="App" sx={{ backgroundColor: '#f4f6f8', minHeight: '100vh' }}>
      <AppBar position="static" sx={{
        background: 'linear-gradient(90deg, #8E2DE2 0%, #DA4453 100%)',
  boxShadow: '0 3px 5px rgba(0,0,0,0.2)'
  //       background: 'linear-gradient(90deg, #43cea2 0%, #185a9d 100%)',
  // boxShadow: '0 3px 5px rgba(0,0,0,0.2)'
      }}>
        <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold', color: '#fff' }}>
  💼 Salary Insights
</Typography>
        </Toolbar>
      </AppBar>

      <Paper elevation={3} sx={{ margin: 3, paddingBottom: 3, borderRadius: 2 }}>
        <Tabs
          value={currentTabIndex}
          onChange={handleTabChange}
          indicatorColor="secondary"
          textColor="primary"
          variant="fullWidth"
          sx={{ backgroundColor: '#fff', borderBottom: '1px solid #ccc' }}
        >
          <Tab label="Dashboard" sx={{ fontWeight: 500 }} />
          <Tab label="Predictions" sx={{ fontWeight: 500 }} />
          <Tab label="Salary Calculator" sx={{ fontWeight: 500 }} />
        </Tabs>

        <Container maxWidth="lg" sx={{ mt: 3 }}>
          {currentTabIndex === 0 && <DashBoard />}
          {currentTabIndex === 1 && <Predictions />}
          {currentTabIndex === 2 && <SalaryCalculator />}
        </Container>
      </Paper>
    </Box>
  );
}

export default App;
