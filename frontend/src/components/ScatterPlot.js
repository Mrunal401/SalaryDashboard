// ScatterChart.js
import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

function ScatterChart({ data }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const scatterData = data.map((item, index) => ({
      x: index,
      y: parseFloat(item.prediction),
      label: item.job_title
    }));

    const labels = data.map(item => item.job_title);

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext("2d");
    chartInstance.current = new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: "Predicted Salary by Job Title",
            data: scatterData,
            backgroundColor: "#36A2EB",
          },
        ],
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const index = context.dataIndex;
                return `${labels[index]}: $${context.raw.y.toFixed(2)}`;
              },
            },
          },
        },
        scales: {
          x: {
            ticks: {
              callback: function (val, index) {
                return labels[index];
              },
            },
            title: {
              display: true,
              text: "Job Title (Index)",
            },
          },
          y: {
            title: {
              display: true,
              text: "Predicted Salary (USD)",
            },
          },
        },
      },
    });
  }, [data]);


  return (
    <div style={{ position: "relative", height: "500px", width: "100%" }}>
      <canvas ref={chartRef}></canvas>
    </div>
  );
}

export default ScatterChart;
