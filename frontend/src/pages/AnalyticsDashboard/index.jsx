import React, { useState, useEffect } from "react";
import Header from "../../components/Commons/Header";
import { Chart } from "react-google-charts";
import "./AnalyticsDashboard.css";

function getRandomNumber() {
  return Math.floor(Math.random() * 100) + 1;
}

function getData() {
  return [
    ["Age", "Weight"],
    ...Array.from({ length: 16 }, () => [getRandomNumber(), getRandomNumber()]),
  ];
}

export const scatterChartOptions = {
  title: "Company Performance",
  legend: { position: "bottom" },
  animation: {
    duration: 1000,
    easing: "out",
  },
  vAxis: {
    title: "Weight",
    viewWindow: { max: 100, min: 0 },
    textStyle: { color: "#000" },
    titleTextStyle: { color: "#000" },
  },
  hAxis: {
    title: "Age",
    viewWindow: { max: 100, min: 0 },
    textStyle: { color: "#000" },
    titleTextStyle: { color: "#000" },
  },
  titleTextStyle: {
    color: "#000",
  },
};

const lineChartData = [
  ["x", "dogs"],
  [0, 0],
  [1, 10],
  [2, 23],
  [3, 17],
  [4, 18],
  [5, 9],
  [6, 11],
  [7, 27],
  [8, 33],
  [9, 40],
  [10, 32],
  [11, 35],
];

const lineChartOptions = {
  title: "Line Chart Example",
  hAxis: {
    title: "Time",
    textStyle: { color: "#000" },
    titleTextStyle: { color: "#000" },
  },
  vAxis: {
    title: "Popularity",
    textStyle: { color: "#000" },
    titleTextStyle: { color: "#000" },
  },
  legend: "none",
};

// Main AnalyticsDashboard component
const AnalyticsDashboard = () => {
  const [chartData, setChartData] = useState(getData);
  const [year, setYear] = useState(new Date().getFullYear());

  useEffect(() => {
    const intervalId = setInterval(() => {
      setChartData(getData());
      setYear((prevYear) => prevYear - 1);
    }, 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, [setChartData]);

  return (
    <div className="dashboard-container">
      <main className="main-container">
        <h2>Welcome, User!</h2>
        <div className="overview-section">
          <div className="overview-card">
            <h3>Overview</h3>
            <p>
              Total Videos Created: <b>23</b>
            </p>
            <p>
              Total Views (All videos): <b>1003</b>{" "}
              <span className="positive">(+13 today)</span>
            </p>
            <p>
              Average Watch time: <b>45 mins</b>
            </p>
            <p>
              Average Completion Rate: <b>83%</b>{" "}
              <span className="negative">(-3%)</span>
            </p>
            <p>
              Total Quiz Attempt Rate: <b>75%</b>
            </p>
            <p>
              Average Quiz Score: <b>6.3</b>
            </p>
          </div>

          <div className="best-videos-card">
            <h3>Best Performing Videos</h3>
            <p>Life Insurance (300 views)</p>
            <div className="progress-bar blue" style={{ width: "80%" }}></div>
            <p>Bajaj Finserv (212 views)</p>
            <div className="progress-bar blue" style={{ width: "60%" }}></div>
            <p>Health Insurance (112 views)</p>
            <div className="progress-bar blue" style={{ width: "40%" }}></div>
          </div>

          <div className="difficult-quiz-card">
            <h3>Most Difficult Quiz</h3>
            <p>Life Insurance (4.2 Avg score)</p>
            <p>Bajaj Finserv (5.3 Avg score)</p>
            <p>Health Insurance (6.4 Avg score)</p>
          </div>
        </div>

        <div className="chart-section">
          <h3>Real-Time Scatter Chart</h3>
          <Chart
            chartType="ScatterChart"
            width="100%"
            height="400px"
            data={chartData}
            options={scatterChartOptions}
          />
          <div style={{ width: "100%", textAlign: "center" }}>{year}</div>
        </div>

        <div className="chart-section">
          <h3>Line Chart Example</h3>
          <Chart
            chartType="LineChart"
            width="100%"
            height="400px"
            data={lineChartData}
            options={lineChartOptions}
          />
        </div>
      </main>
    </div>
  );
};

export default AnalyticsDashboard;
