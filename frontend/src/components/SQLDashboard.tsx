import React, { useState, useEffect } from "react";
import {
  sqlAPI,
  QueryRequest,
  SQLResponse,
  HealthResponse,
} from "../services/api";
import "./SQLDashboard.css";

const SQLDashboard: React.FC = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SQLResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [maxTables, setMaxTables] = useState(3);

  useEffect(() => {
    // Check API health on component mount
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const healthData = await sqlAPI.getHealth();
      setHealth(healthData);
    } catch (err) {
      console.error("Health check failed:", err);
    }
  };

  const executeQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a query");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const request: QueryRequest = {
        question: query,
        max_tables: maxTables,
      };

      const response = await sqlAPI.executeQuery(request);
      setResult(response);
    } catch (err) {
      console.error("Query execution error:", err);
      if (err instanceof Error) {
        setError(`Error: ${err.message}`);
      } else if (typeof err === "object" && err !== null && "response" in err) {
        const axiosError = err as {
          response?: { data?: { detail?: string }; status?: number };
        };
        if (axiosError.response?.data?.detail) {
          setError(`API Error: ${axiosError.response.data.detail}`);
        } else {
          setError(`HTTP Error: ${axiosError.response?.status || "Unknown"}`);
        }
      } else {
        setError("An unexpected error occurred while executing the query");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      executeQuery();
    }
  };

  const clearResults = () => {
    setResult(null);
    setError(null);
  };

  const formatJSON = (obj: unknown) => {
    try {
      return JSON.stringify(obj, null, 2);
    } catch {
      return String(obj);
    }
  };

  return (
    <div className="sql-dashboard">
      <header className="dashboard-header">
        <h1>E-commerce SQL Agent Dashboard</h1>
        <div className="health-status">
          {health ? (
            <div className={`status-indicator ${health.status}`}>
              <span className="status-dot"></span>
              {health.status} - {health.total_tables} tables available
            </div>
          ) : (
            <div className="status-indicator unknown">
              <span className="status-dot"></span>
              Checking connection...
            </div>
          )}
        </div>
      </header>

      <div className="dashboard-content">
        <div className="query-section">
          <div className="query-header">
            <h2>Enter your query</h2>
            <div className="query-controls">
              <label>
                Max Tables:
                <select
                  value={maxTables}
                  onChange={(e) => setMaxTables(Number(e.target.value))}
                >
                  <option value={1}>1</option>
                  <option value={3}>3</option>
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                </select>
              </label>
            </div>
          </div>

          <div className="query-input-container">
            <textarea
              className="query-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask a question about the e-commerce data...&#10;&#10;Examples:&#10;• What are the top 5 selling products?&#10;• Show me customer orders from last month&#10;• Which products have the highest ratings?&#10;&#10;Press Ctrl+Enter to execute"
              rows={6}
            />
          </div>

          <div className="query-actions">
            <button
              className="execute-btn"
              onClick={executeQuery}
              disabled={loading || !query.trim()}
            >
              {loading ? "Executing..." : "Execute Query"}
            </button>
            <button
              className="clear-btn"
              onClick={clearResults}
              disabled={!result && !error}
            >
              Clear Results
            </button>
          </div>
        </div>

        {error && (
          <div className="error-section">
            <h3>Error</h3>
            <div className="error-content">
              <pre>{error}</pre>
            </div>
          </div>
        )}

        {result && (
          <div className="results-section">
            <h2>Query Results</h2>

            <div className="result-card">
              <h3>Question</h3>
              <div className="result-content">
                <p>{query}</p>
              </div>
            </div>

            <div className="result-card">
              <h3>Database Used</h3>
              <div className="result-content">
                <span className="db-tag">{result.db}</span>
              </div>
            </div>

            <div className="result-card">
              <h3>Answer</h3>
              <div className="result-content">
                <p
                  style={{
                    fontSize: "1.1rem",
                    fontWeight: "500",
                    color: "#1e293b",
                  }}
                >
                  {result.answer}
                </p>
              </div>
            </div>

            {result.sql_query &&
              result.sql_query !== "No SQL query found in execution steps" && (
                <div className="result-card">
                  <h3>Generated SQL Query</h3>
                  <div className="result-content">
                    <pre className="sql-code">{result.sql_query}</pre>
                  </div>
                </div>
              )}

            {result.intermediate_steps &&
              result.intermediate_steps.length > 0 && (
                <div className="result-card">
                  <h3>Intermediate Steps</h3>
                  <div className="result-content">
                    <pre className="json-result">
                      {formatJSON(result.intermediate_steps)}
                    </pre>
                  </div>
                </div>
              )}
          </div>
        )}

        {health && (
          <div className="info-section">
            <h2>Database Information</h2>
            <div className="info-grid">
              <div className="info-card">
                <h4>Available Databases</h4>
                <div className="databases-list">
                  {health.databases && health.databases.length > 0 ? (
                    health.databases.map((db, index) => (
                      <span key={index} className="db-tag">
                        {db}
                      </span>
                    ))
                  ) : (
                    <span className="db-tag">No databases available</span>
                  )}
                </div>
              </div>
              <div className="info-card">
                <h4>Available Tables ({health.total_tables || 0})</h4>
                <div className="tables-grid">
                  {health.available_tables &&
                  health.available_tables.length > 0 ? (
                    <>
                      {health.available_tables
                        .slice(0, 10)
                        .map((table, index) => (
                          <span key={index} className="table-item">
                            {table}
                          </span>
                        ))}
                      {health.available_tables.length > 10 && (
                        <span className="table-item more">
                          ...and {health.available_tables.length - 10} more
                        </span>
                      )}
                    </>
                  ) : (
                    <span className="table-item">No tables available</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SQLDashboard;
