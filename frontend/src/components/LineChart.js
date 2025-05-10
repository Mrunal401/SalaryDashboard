import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';


function LineChartFromJSON({ data, chartId }) {
    const [chartData, setChartData] = useState(null);
    const chartRef = useRef(null);
    console.log("jsonData", data);

  useEffect(() => {

    const prepareChartDataFromJSON = () => {
        try {
          const labels = data.map(item => item.job_title); // assuming job_title is the label
          const salaryData = data.map(item => parseFloat(item.avg_salary)); // assuming average_salary is the field

        setChartData({
            labels: labels,
            datasets: [{
              label: 'Average Salary',
              data: salaryData,
              fill: false,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.3,
              pointRadius: 5,
              pointHoverRadius: 7
            }]
          });
      } catch (error) {
        console.error('Error preparing chart data from JSON:', error);
      }
    };

    prepareChartDataFromJSON();
  }, [data]);

  useEffect(() => {
    // Function to draw chart
    const drawChart = () => {
      if (chartData) {
        // Destroy previous chart instance if it exists
        if (chartRef.current) {
          chartRef.current.destroy();
        }

        // Create new chart instance
        const ctx = document.getElementById(chartId);
        chartRef.current = new Chart(ctx, {
          //type: 'bar',
          type: 'line',
          data: chartData,
          options: {
            scales: {
              y: {
                // beginAtZero: true
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Average Salary'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Job Title'
                }
              }
            }
          }
        });
      }
    };

    drawChart();

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [chartData, chartId]);

  return <canvas id={chartId} width="400" height="400"></canvas>;
}

//export default BarChartFromJSON;
export default LineChartFromJSON;
