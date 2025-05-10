import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';


export default function HistogramChart({ data, chartId }) {
    const chartInstance = useRef(null);
  
    useEffect(() => {
      // Clean up previous chart instance if it exists
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
  
      if (!data || data.length === 0) {
        console.warn('No data provided for histogram');
        return;
      }
  
      try {
        const ctx = document.getElementById(chartId);
        if (!ctx) {
          console.error(`Canvas element with id ${chartId} not found`);
          return;
        }
  
        // Log the first few items to understand the data structure
        console.log("Histogram data sample:", data.slice(0, 3));
  
        // Process the data based on your specific structure
        // Assuming your data has job_title, experience_level, and avg_salary fields
        
        // Get unique job titles (limit to top 8 for readability)
        const jobTitles = [...new Set(data
          .map(item => item.job_title)
          .filter(Boolean))]
          .slice(0, 8);
        
        // Get unique experience levels
        const experienceLevels = [...new Set(data
          .map(item => item.experience_level)
          .filter(Boolean))];
        
        // Fixed colors for experience levels
        const colorMap = {
          'Entry-level': 'rgba(152, 251, 152, 0.7)',
          'Mid-level': 'rgba(255, 182, 193, 0.7)',
          'Senior': 'rgba(186, 85, 211, 0.7)',
          'Executive': 'rgba(144, 151, 238, 0.7)',
        };
  
        // Create datasets for each experience level
        const datasets = experienceLevels.map(level => {
          return {
            label: level,
            data: jobTitles.map(title => {
              const matchingItems = data.filter(item => 
                item.job_title === title && 
                item.experience_level === level
              );
              
              if (matchingItems.length > 0) {
                return parseFloat(matchingItems[0].avg_salary) || 0;
              }
              return 0;
            }),
            backgroundColor: colorMap[level] || `rgba(${Math.floor(Math.random() * 200)}, ${Math.floor(Math.random() * 200)}, ${Math.floor(Math.random() * 200)}, 0.7)`,
          };
        });
  
        // Create the chart
        chartInstance.current = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: jobTitles,
            datasets: datasets
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Top Paying Job Titles by Experience Level',
                font: {
                  size: 16
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                      label += ': ';
                    }
                    if (context.parsed.y !== null) {
                      label += new Intl.NumberFormat('en-US', { 
                        style: 'currency', 
                        currency: 'USD',
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0
                      }).format(context.parsed.y);
                    }
                    return label;
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Average Salary ($)',
                  font: {
                    size: 14
                  }
                },
                ticks: {
                  callback: function(value) {
                    return '$' + value.toLocaleString();
                  }
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Job Title',
                  font: {
                    size: 14
                  }
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            }
          }
        });
      } catch (error) {
        console.error('Error creating histogram chart:', error);
      }
  
      // Clean up on unmount
      return () => {
        if (chartInstance.current) {
          chartInstance.current.destroy();
        }
      };
    }, [data, chartId]);
  
    return (
      <div style={{ width: '100%', height: '100%' }}>
        <canvas id={chartId} style={{ width: '100%', height: '100%' }}></canvas>
      </div>
    );
  }
