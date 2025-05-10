import { Box, Button, Card, CardActions, CardContent, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { useState } from "react";
import { fetchCSVFromS3 } from "../utils/fetchCSVFromS3";
import ScatterChart from "./ScatterPlot";

export default function Predictions(props) {
    const [testData, setTestData] = useState([]);
    const [trainData, setTrainData] = useState([]);
    const [compar, setCompar] = useState([]);
    const [predictionData, setPredictionData] = useState([]);
    const [scatterData, setScatterData] = useState([]);

      

    const handleTrainingData = async () => {

        const data = await fetchCSVFromS3('mrunalproj', 'output3/train_data/part-00000-7c08f0d8-**.csv');
        console.log("training data from S3", data);
        setTrainData(data);

    };

    const handleTestData = async () => {

        const data = await fetchCSVFromS3('mrunalproj', 'output3/test_data/part-00000-464c3032-**.csv');
        console.log("training data from S3", data);
        setTestData(data);

    };

    const handleCompare = async () => {

        const data = await fetchCSVFromS3('mrunalproj', 'output3/predictions1/part-00000-94d1ba95-**.csv');
        console.log("training data from S3", data);
        setCompar(data);

    };

    
    const handleScatterChartData = async () => {
        const data = await fetchCSVFromS3('mrunalproj', 'output3/predictions1/part-00000-94d1ba95-**.csv');
        console.log("data from S3", data);
        setScatterData(data);

    };

  return (
    <Box sx={{ backgroundColor: "#f0f2f5", minHeight: "100vh", padding: "40px" }}>
      <Typography variant="h5" align="center" gutterBottom sx={{ color: "#2e3a59", fontWeight: "bold" }}>
        Machine Learning-Based Salary Predictions
      </Typography>
      <Typography align="center" color="textSecondary" sx={{ mb: 4 }}>
        Salary is predicted using a regression model. Training (70%) and testing (30%) datasets are built using features like job title, location, experience level, and work setting.
      </Typography>

      {/* First Row: Training and Testing Tables */}
      <Box display="flex" justifyContent="center" gap={4} flexWrap="wrap" mb={4}>
        <Card sx={{ maxWidth: 500, maxHeight: 500, borderRadius: 3, boxShadow: 4 }}>
          <CardActions sx={{ justifyContent: "center" }}>
            <Button
              onClick={handleTrainingData}
              sx={{
                backgroundColor: "#4B6CB7",
                '&:hover': { backgroundColor: "#3a539b" },
                color: "#fff"
              }}
            >
              Load Training Data
            </Button>
          </CardActions>
          <CardContent sx={{ overflowY: 'auto', maxHeight: 400 }}>
            {trainData.length > 0 &&
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      {Object.keys(trainData[0]).map((key) => (
                        <TableCell key={key}>{key}</TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {trainData.map((row, index) => (
                      <TableRow key={index}>
                        {Object.values(row).map((val, idx) => (
                          <TableCell key={idx}>{val}</TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            }
          </CardContent>
        </Card>

        <Card sx={{ maxWidth: 500, maxHeight: 500, borderRadius: 3, boxShadow: 4 }}>
          <CardActions sx={{ justifyContent: "center" }}>
            <Button
              onClick={handleTestData}
              sx={{
                backgroundColor: "#182848",
                '&:hover': { backgroundColor: "#0f1e35" },
                color: "#fff"
              }}
            >
              Load Test Data
            </Button>
          </CardActions>
          <CardContent sx={{ overflowY: 'auto', maxHeight: 400 }}>
            {testData.length > 0 &&
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      {Object.keys(testData[0]).map((key) => (
                        <TableCell key={key}>{key}</TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {testData.map((row, index) => (
                      <TableRow key={index}>
                        {Object.values(row).map((val, idx) => (
                          <TableCell key={idx}>{val}</TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            }
          </CardContent>
        </Card>
      </Box>

      {/* Second Row: Scatter Plot and Prediction Table */}
      <Box display="flex" justifyContent="center" gap={4} flexWrap="wrap">
        <Card sx={{ width: 1000, height: 600, borderRadius: 3, boxShadow: 4 }}>
          <CardActions sx={{ justifyContent: "center" }}>
            <Button
              onClick={handleScatterChartData}
              sx={{
                backgroundColor: "#20c997",
                '&:hover': { backgroundColor: "#1aa884" },
                color: "#fff"
              }}
            >
              Load Predicted Salary by Job
            </Button>
          </CardActions>
          <CardContent>
            {scatterData.length > 0 && (
              <Box sx={{ width: '100%', height: '100%' }}>
                <ScatterChart data={scatterData} />
              </Box>
            )}
          </CardContent>
        </Card>

        <Card sx={{ maxWidth: 500, maxHeight: 500, borderRadius: 3, boxShadow: 4 }}>
          <CardActions sx={{ justifyContent: "center" }}>
            <Button
              onClick={handleCompare}
              sx={{
                backgroundColor: "#6c63ff",
                '&:hover': { backgroundColor: "#5b52d1" },
                color: "#fff"
              }}
            >
              Compare Actual vs Predicted
            </Button>
          </CardActions>
          <CardContent sx={{ overflowY: 'auto', maxHeight: 400 }}>
            {compar.length > 0 &&
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      {Object.keys(compar[0]).map((key) => (
                        <TableCell key={key}>{key}</TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {compar.map((row, index) => (
                      <TableRow key={index}>
                        {Object.values(row).map((val, idx) => (
                          <TableCell key={idx}>{val}</TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            }
          </CardContent>
        </Card>
      </Box>
    </Box>
  );

}

