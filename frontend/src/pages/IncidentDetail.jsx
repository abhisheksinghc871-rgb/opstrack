import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { commentsApi, incidentsApi, usersApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import ErrorBanner from "../components/ErrorBanner.jsx";

const STATUS_OPTIONS = ["open", "investigating", "mitigated", "resolved", "closed"];
const SEVERITY_OPTIONS = ["sev1", "sev2", "sev3", "sev4"];

export default function IncidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState(null);
  const [users, setUsers] = useState([]);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const [incidentRes, usersRes, commentsRes] = await Promise.all([
        incidentsApi.get(id),
        usersApi.list(),
        commentsApi.list("incident", id),
      ]);
      setIncident(incidentRes.data);
      setUsers(usersRes.data);
      setComments(commentsRes.data);
      setError("");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const updateField = async (field, value) => {
    try {
      const res = await incidentsApi.update(id, { [field]: value });
      setIncident(res.data);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    try {
      await commentsApi.create("incident", id, newComment.trim());
      setNewComment("");
      const res = await commentsApi.list("incident", id);
      setComments(res.data);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this incident? This cannot be undone.")) return;
    try {
      await incidentsApi.remove(id);
      navigate("/incidents");
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const userName = (uid) => users.find((u) => u.id === uid)?.full_name || "Unassigned";

  if (loading) return <div className="page-container loading-state">Loading incident...</div>;
  if (!incident)
    return (
      <div className="page-container">
        <ErrorBanner message={error || "Incident not found"} />
      </div>
    );

  return (
    <div className="page-container">
      <Link to="/incidents" className="back-link">← Back to incidents</Link>
      <div className="page-header">
        <h1>{incident.title}</h1>
        <button className="btn btn-danger btn-small" onClick={handleDelete}>
          Delete incident
        </button>
      </div>
      <ErrorBanner message={error} />

      <div className="detail-grid">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Description</h3>
          <p style={{ color: "var(--color-text-muted)", whiteSpace: "pre-wrap" }}>
            {incident.description || "No description provided."}
          </p>

          <h3>Comments</h3>
          {comments.length === 0 && <p className="empty-state">No comments yet.</p>}
          {comments.map((c) => (
            <div className="comment" key={c.id}>
              <div className="comment-meta">
                {userName(c.author_id)} · {new Date(c.created_at).toLocaleString()}
              </div>
              <div>{c.body}</div>
            </div>
          ))}
          <form onSubmit={handleAddComment} style={{ marginTop: 12 }}>
            <div className="form-group">
              <textarea
                placeholder="Add an update..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
              />
            </div>
            <button className="btn btn-small" type="submit">
              Post comment
            </button>
          </form>
        </div>

        <div className="card">
          <h3 style={{ marginTop: 0 }}>Details</h3>
          <div className="field-row">
            <span>Status</span>
            <select value={incident.status} onChange={(e) => updateField("status", e.target.value)}>
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s.replace("_", " ")}
                </option>
              ))}
            </select>
          </div>
          <div className="field-row">
            <span>Severity</span>
            <select value={incident.severity} onChange={(e) => updateField("severity", e.target.value)}>
              {SEVERITY_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <div className="field-row">
            <span>Assigned to</span>
            <select
              value={incident.assigned_to_id || ""}
              onChange={(e) => updateField("assigned_to_id", e.target.value || null)}
            >
              <option value="">Unassigned</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name}
                </option>
              ))}
            </select>
          </div>
          <div className="field-row">
            <span>Created by</span>
            <span>{userName(incident.created_by_id)}</span>
          </div>
          <div className="field-row">
            <span>Created</span>
            <span>{new Date(incident.created_at).toLocaleDateString()}</span>
          </div>
          {incident.resolved_at && (
            <div className="field-row">
              <span>Resolved</span>
              <span>{new Date(incident.resolved_at).toLocaleDateString()}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
