import { useEffect, useState } from "react";
import { dashboardApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import ErrorBanner from "../components/ErrorBanner.jsx";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardApi
      .stats()
      .then((res) => setStats(res.data))
      .catch((err) => setError(extractErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>
      <ErrorBanner message={error} />
      {loading && <div className="loading-state">Loading dashboard...</div>}

      {stats && (
        <>
          <div className="grid grid-stats" style={{ marginBottom: 24 }}>
            <StatCard label="Total tasks" value={stats.total_tasks} />
            <StatCard label="Total incidents" value={stats.total_incidents} />
            <StatCard label="Open incidents" value={stats.open_incidents} />
            <StatCard label="Stale tasks (7d+)" value={stats.overdue_looking_tasks} />
          </div>

          <div className="grid" style={{ gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Tasks by status</h3>
              <BreakdownList data={stats.tasks_by_status} />
            </div>
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Tasks by priority</h3>
              <BreakdownList data={stats.tasks_by_priority} />
            </div>
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Incidents by status</h3>
              <BreakdownList data={stats.incidents_by_status} />
            </div>
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Incidents by severity</h3>
              <BreakdownList data={stats.incidents_by_severity} />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="card stat-card">
      <span className="stat-value">{value}</span>
      <span className="stat-label">{label}</span>
    </div>
  );
}

function BreakdownList({ data }) {
  const entries = Object.entries(data || {});
  if (entries.length === 0) {
    return <p className="empty-state" style={{ padding: "10px 0" }}>No data yet</p>;
  }
  return (
    <div>
      {entries.map(([key, value]) => (
        <div className="field-row" key={key}>
          <span style={{ textTransform: "capitalize" }}>{key.replace("_", " ")}</span>
          <span>{value}</span>
        </div>
      ))}
    </div>
  );
}
