import React, { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
import {
  Trophy,
  Target,
  Clock,
  Zap,
  Book,
  Brain,
  AlertCircle,
} from "lucide-react";
import "./Result.css";

const Result = ({
  finalScore,
  correctAnswers,
  totalQuestions,
  highestStreak,
  timeSpent,
  quizResults,
  onRestart,
}) => {
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  const incorrectAnswers = totalQuestions - correctAnswers;
  const averageTime = Math.round(
    timeSpent.reduce((a, b) => a + b, 0) / totalQuestions
  );

  // Performance chart data
  const performanceData = [
    { name: "Correct", value: correctAnswers },
    { name: "Incorrect", value: incorrectAnswers },
  ];

  // Time distribution data
  const timeData = timeSpent.map((time, index) => ({
    question: `Q${index + 1}`,
    time: time,
  }));

  const COLORS = ["#4CAF50", "#F44336"];

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        if (
          !quizResults ||
          !quizResults.questions ||
          !quizResults.user_answers
        ) {
          throw new Error("Missing required quiz data");
        }

        const questionsLength = quizResults.questions.length;
        const answersLength = quizResults.user_answers.length;
        const timesLength = quizResults.question_times.length;

        console.log("Debug lengths:", {
          questions: questionsLength,
          answers: answersLength,
          times: timesLength,
        });

        if (
          questionsLength !== answersLength ||
          questionsLength !== timesLength
        ) {
          throw new Error(
            `Data length mismatch: Questions (${questionsLength}), Answers (${answersLength}), Times (${timesLength})`
          );
        }

        const formattedQuestions = quizResults.questions.map(
          (question, index) => {
            if (
              !question.question ||
              !question.options ||
              !question.correctAnswer
            ) {
              throw new Error(`Invalid question data at index ${index}`);
            }
            return {
              question: question.question,
              options: question.options,
              correctAnswer: question.correctAnswer,
              type: question.type || "mcq",
              difficulty: question.difficulty || "Medium",
              explanation: question.explanation || "",
            };
          }
        );

        const formattedUserAnswers = quizResults.user_answers.map(
          (answer, index) => {
            return {
              selected_answer: answer.selected_answer || null,
              answered: Boolean(answer.answered),
            };
          }
        );

        const formattedTimes = quizResults.question_times.map((time, index) => {
          const numberTime = Number(time);
          if (isNaN(numberTime)) {
            throw new Error(`Invalid time value at index ${index}`);
          }
          return numberTime;
        });

        const requestData = {
          topic: quizResults.topic || "General Knowledge",
          questions: formattedQuestions,
          user_answers: formattedUserAnswers,
          question_times: formattedTimes,
        };

        console.log(
          "Sending request data:",
          JSON.stringify(requestData, null, 2)
        );

        const response = await fetch("http://127.0.0.1:8000/analyze-quiz/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          throw new Error(
            errorData?.message ||
              `Server responded with status ${response.status}`
          );
        }

        const data = await response.json();
        if (!data || !data.data) {
          throw new Error("Invalid response format from server");
        }

        setAnalysis(data.data);
        setError(null);
      } catch (err) {
        console.error("Analysis fetch error details:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (quizResults) {
      fetchAnalysis();
    }
  }, [quizResults]);

  const getProficiencyColor = (level) => {
    const colors = {
      Beginner: "#FFA726",
      Intermediate: "#66BB6A",
      Advanced: "#42A5F5",
      Expert: "#AB47BC",
    };
    return colors[level] || "#78909C";
  };

  const renderDebugInfo = () => {
    if (!quizResults) return null;

    return (
      <div className="debug-info" style={{ display: "none" }}>
        <pre>
          {JSON.stringify(
            {
              questionsLength: quizResults.questions?.length,
              answersLength: quizResults.user_answers?.length,
              timesLength: quizResults.question_times?.length,
              topic: quizResults.topic,
            },
            null,
            2
          )}
        </pre>
      </div>
    );
  };

  return (
    <div className="result-container">
      {renderDebugInfo()}

      {error && (
        <div className="analysis-error">
          <AlertCircle className="error-icon" size={24} />
          <div>
            <p>Error loading analysis: {error}</p>
            <p className="text-sm text-gray-600">
              Please check that all questions have corresponding answers and
              times.
            </p>
          </div>
        </div>
      )}

      <h2 className="result-title">Quiz Results</h2>

      {/* Statistics Grid */}
      <div className="result-grid">
        <div className="result-item result-score">
          <Trophy className="result-icon" size={24} />
          <p className="result-label">Final Score</p>
          <p className="result-value">{finalScore}</p>
        </div>
        <div className="result-item result-accuracy">
          <Target className="result-icon" size={24} />
          <p className="result-label">Accuracy</p>
          <p className="result-value">
            {Math.round((correctAnswers / totalQuestions) * 100)}%
          </p>
        </div>
        <div className="result-item result-streak">
          <Zap className="result-icon" size={24} />
          <p className="result-label">Highest Streak</p>
          <p className="result-value">{highestStreak}</p>
        </div>
        <div className="result-item result-time">
          <Clock className="result-icon" size={24} />
          <p className="result-label">Avg. Time per Question</p>
          <p className="result-value">{averageTime}s</p>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-card">
          <h3 className="chart-title">Answer Distribution</h3>
          <div className="pie-chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={performanceData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                >
                  {performanceData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="chart-legend">
              <div className="legend-item">
                <div
                  className="legend-color"
                  style={{ color: COLORS[0] }}
                ></div>
                <span>Correct ({correctAnswers})</span>
              </div>
              <div className="legend-item">
                <div
                  className="legend-color"
                  style={{ color: COLORS[1] }}
                ></div>
                <span>Incorrect ({incorrectAnswers})</span>
              </div>
            </div>
          </div>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Time Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={timeData}>
              <XAxis dataKey="question" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="time" fill="#64B5F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {loading ? (
        <div className="analysis-loading">
          <div className="loading-spinner"></div>
          <p>Analyzing your performance...</p>
        </div>
      ) : error ? (
        <div className="analysis-error">
          <AlertCircle className="error-icon" size={24} />
          <p>Error loading analysis: {error}</p>
        </div>
      ) : (
        analysis && (
          <div className="analysis-section">
            <h3 className="analysis-title">
              <Brain className="inline-icon" size={24} />
              Detailed Performance Analysis
            </h3>

            <div className="analysis-time-management">
              <div className="analysis-card proficiency">
                <div className="proficiency-header">
                  <h4>Overall Proficiency</h4>
                  <span
                    className="proficiency-badge"
                    style={{
                      color: getProficiencyColor(
                        analysis.overall_performance.proficiency_level
                      ),
                      border: "solid",
                      borderRadius: "10px",
                    }}
                  >
                    {analysis.overall_performance.proficiency_level}
                  </span>
                </div>

                <div className="strengths-weaknesses">
                  <div className="strengths">
                    <h5>Strengths</h5>
                    <ul>
                      {analysis.overall_performance.strengths.map(
                        (strength, index) => (
                          <li key={index}>{strength}</li>
                        )
                      )}
                    </ul>
                  </div>
                  <div className="weaknesses">
                    <h5>Areas for Improvement</h5>
                    <ul>
                      {analysis.overall_performance.weaknesses.map(
                        (weakness, index) => (
                          <li key={index}>{weakness}</li>
                        )
                      )}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="analysis-card time-management">
                <h4>
                  <Clock className="inline-icon" size={20} />
                  Time Management Analysis
                </h4>
                <p className="time-assessment">
                  {analysis.time_management.time_management_assessment}
                </p>
                <div className="recommendations">
                  <h5>Recommendations</h5>
                  <ul>
                    {analysis.time_management.recommendations.map(
                      (rec, index) => (
                        <li key={index}>{rec}</li>
                      )
                    )}
                  </ul>
                </div>
              </div>
            </div>

            <div className="topic-analysis-container">
              <h4 className="topic-analysis-title">
                <Book className="inline-icon" size={20} />
                Topic-wise Analysis
              </h4>
              <div className="topic-cards-grid">
                {analysis.topic_wise_analysis.map((topic, index) => (
                  <div key={index} className="topic-card">
                    <div className="topic-card-header">
                      <h5>{topic.topic}</h5>
                      <span
                        className="mastery-badge"
                        style={{
                          color: getProficiencyColor(topic.mastery_level),
                          border: "solid",
                          borderRadius: "10px",
                        }}
                      >
                        {topic.mastery_level}
                      </span>
                    </div>

                    <div className="revision-points">
                      <h6>Key Revision Points</h6>
                      <ul>
                        {topic.revision_points.map((point, idx) => (
                          <li key={idx}>{point}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="resources">
                      <h6>Recommended Resources</h6>
                      <ul>
                        {topic.recommended_resources.map((resource, idx) => (
                          <li key={idx}>{resource}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )
      )}

      <button className="restart-button" onClick={onRestart}>
        Restart Quiz
      </button>
    </div>
  );
};

export default Result;
