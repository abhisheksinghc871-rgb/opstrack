import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { incidentsApi, usersApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import ErrorBanner from "../components/ErrorBanner.jsx";
import Badge from "../components/Badge.jsx";

const STATUS_OPTIONS = ["open", "investigating", "mitigated", "resolved", "closed"];
const SEVERITY_OPTIONS = ["sev1", "sev2", "sev3", "sev4"];

export default function Incidents() {
  const navigate = useNavigate();
  const [incidents, setIncidents] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [severityFilter, setSeverityFilter] = useState("");
  const [showForm, setShowForm] = useState(false);

  const loadIncidents = async () => {
    setLoading(true);
    try {
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (severityFilter) params.severity = severityFilter;
      const res = await incidentsApi.list(params);
      setIncidents(res.data);
      setError("");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    usersApi.list().then((res) => setUsers(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    loadIncidents();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, severityFilter]);

  const userName = (id) => users.find((u) => u.id === id)?.full_name || "Unassigned";

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Incidents</h1>
        <button className="btn" onClick={() => setShowForm((v) => !v)}>
          {showForm ? "Cancel" : "New Incident"}
        </button>
      </div>

      <ErrorBanner message={error} />

      {showForm && (
        <IncidentForm
          users={users}
          onCreated={() => {
            setShowForm(false);
            loadIncidents();
          }}
        />
      )}

      <div className="filters-bar">
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All statuses</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s.replace("_", " ")}
            </option>
          ))}
        </select>
        <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
          <option value="">All severities</option>
          {SEVERITY_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      <div className="card" style={{ padding: 0 }}>
        {loading ? (
          <div className="loading-state">Loading incidents...</div>
        ) : incidents.length === 0 ? (
          <div className="empty-state">No incidents. All quiet.</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Severity</th>
                <th>Assigned to</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map((incident) => (
                <tr
                  key={incident.id}
                  className="clickable-row"
                  onClick={() => navigate(`/incidents/${incident.id}`)}
                >
                  <td>{incident.title}</td>
                  <td>
                    <Badge type="status" value={incident.status} />
                  </td>
                  <td>
                    <Badge type="severity" value={incident.severity} />
                  </td>
                  <td>{userName(incident.assigned_to_id)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function IncidentForm({ users, onCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("sev3");
  const [assignedTo, setAssignedTo] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await incidentsApi.create({
        title,
        description,
        severity,
        assigned_to_id: assignedTo || null,
      });
      onCreated();
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: 20 }}>
      <ErrorBanner message={error} />
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Severity</label>
          <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
            {SEVERITY_OPTIONS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Assign to</label>
          <select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)}>
            <option value="">Unassigned</option>
            {users.map((u) => (
              <option key={u.id} value={u.id}>
                {u.full_name}
              </option>
            ))}
          </select>
        </div>
        <button className="btn" type="submit" disabled={submitting}>
          {submitting ? "Creating..." : "Create incident"}
        </button>
      </form>
    </div>
  );
}
