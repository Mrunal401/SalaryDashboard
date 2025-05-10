import { Box, Button, Card, CardActions, CardContent, Typography, Grid, useTheme } from "@mui/material";
import { useState } from "react";
import { fetchCSVFromS3 } from "../utils/fetchCSVFromS3";
import LineChartFromJSON from "./LineChart";
import DonutChart from "./DonutChart"; // Add this import at the top
import HistogramChart from "./HistogramChart";

export default function Dashboard(props) {
    const [lineData, setLineData] = useState([]);
    const [histogramData, setHistogramData] = useState([]);
    const [donutData, setDonutData] = useState([]);
    const theme = useTheme();


    const handleLineChartData = async () => {
        const data = await fetchCSVFromS3('mrunalproj', 'output1/top10_highest_paying_jobs/part-00000-0fa0441c-**.csv');
        console.log("data from S3", data);
        setLineData(data);

    };

    const handleHistogramData = async () => {
      const data = await fetchCSVFromS3('mrunalproj', 'output1/top_by_experience_level/part-00000-14fe1e69-99c6-**.csv');
      console.log("histogram data from S3", data);
      setHistogramData(data);
    };

    const handleDonutChartData = async () => {
      const data = await fetchCSVFromS3('mrunalproj', 'output1/work_setting_distribution/part-00000-859224cd-**.csv');
      console.log("donut data from S3", data);
      setDonutData(data);
    };
    
    return (
      <Box sx={{ padding: "40px", backgroundColor: "#f0f2f5", minHeight: "100vh" }}>
        <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 'bold', color: "#2e3a59" }}>
          Global Tech Salary Dashboard
        </Typography>
  
        <Grid container spacing={4} justifyContent="center" mt={2}>
          {/* Histogram Chart */}
          <Grid item xs={12}>
            <Card sx={{ borderRadius: 3, boxShadow: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom align="center" sx={{ color: "#4B6CB7" }}>
                  Experience Level vs Salary Distribution
                </Typography>
                <CardActions sx={{ justifyContent: "center", mb: 2 }}>
                  <Button 
                    onClick={handleHistogramData} 
                    //variant="contained" color="secondary"
                    sx={{
                      backgroundColor: "#4B6CB7",
                      '&:hover': { backgroundColor: "#3a539b" },
                      color: "#fff"
                    }}>
                    Load Histogram
                  </Button>
                </CardActions>
                {histogramData.length > 0 && (
                  <Box sx={{ height: "500px" }}>
                    <HistogramChart data={histogramData} chartId="histogramChart" />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
  
          {/* Line and Donut Charts Side by Side */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, boxShadow: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom align="center" sx={{ color: "#182848" }}>
                  Top 10 Highest Paying Job Titles
                </Typography>
                <CardActions sx={{ justifyContent: "center", mb: 2 }}>
                  <Button onClick={handleLineChartData} 
                  //variant="contained" color="primary"
                  sx={{
                    backgroundColor: "#182848",
                    '&:hover': { backgroundColor: "#0f1e35" },
                    color: "#fff"
                  }}
                  >
                    Load Line Chart
                  </Button>
                </CardActions>
                {lineData.length > 0 && (
                  <Box sx={{ height: "400px" }}>
                    <LineChartFromJSON data={lineData} chartId="lineChart" />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
  
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, boxShadow: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom align="center" sx={{ color: "#20c997" }}>
                  Work Setting Distribution (Remote, Office, Hybrid)
                </Typography>
                <CardActions sx={{ justifyContent: "center", mb: 2 }}>
                  <Button onClick={handleDonutChartData} 
                  //variant="contained" color="success"
                  sx={{
                    backgroundColor: "#20c997",
                    '&:hover': { backgroundColor: "#1aa884" },
                    color: "#fff"
                  }}
                  >
                    Load Donut Chart
                  </Button>
                </CardActions>
                {donutData.length > 0 && (
                  <Box sx={{ height: "400px" }}>
                    <DonutChart data={donutData} chartId="donutChart" />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
}