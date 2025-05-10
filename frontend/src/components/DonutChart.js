// DonutChart.js
import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function DonutChart({ data, chartId }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const labels = data.map(item => item.work_setting);
    const counts = data.map(item => parseInt(item.count));

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext("2d");

    chartInstance.current = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          label: 'Work Setting Distribution',
          data: counts,
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'right'
          },
          title: {
            display: true,
            text: 'Work Setting Distribution'
          }
        }
      }
    });
  }, [data]);

  return <canvas id={chartId} ref={chartRef} />;
}
