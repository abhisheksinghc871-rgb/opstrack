import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { commentsApi, tasksApi, usersApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import ErrorBanner from "../components/ErrorBanner.jsx";
import Badge from "../components/Badge.jsx";
import { useAuth } from "../context/AuthContext.jsx";

const STATUS_OPTIONS = ["todo", "in_progress", "blocked", "done"];
const PRIORITY_OPTIONS = ["low", "medium", "high", "critical"];

export default function TaskDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [task, setTask] = useState(null);
  const [users, setUsers] = useState([]);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const [taskRes, usersRes, commentsRes] = await Promise.all([
        tasksApi.get(id),
        usersApi.list(),
        commentsApi.list("task", id),
      ]);
      setTask(taskRes.data);
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
      const res = await tasksApi.update(id, { [field]: value });
      setTask(res.data);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    try {
      await commentsApi.create("task", id, newComment.trim());
      setNewComment("");
      const res = await commentsApi.list("task", id);
      setComments(res.data);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this task? This cannot be undone.")) return;
    try {
      await tasksApi.remove(id);
      navigate("/tasks");
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  const userName = (uid) => users.find((u) => u.id === uid)?.full_name || "Unassigned";

  if (loading) return <div className="page-container loading-state">Loading task...</div>;
  if (!task) return <div className="page-container"><ErrorBanner message={error || "Task not found"} /></div>;

  return (
    <div className="page-container">
      <Link to="/tasks" className="back-link">← Back to tasks</Link>
      <div className="page-header">
        <h1>{task.title}</h1>
        <button className="btn btn-danger btn-small" onClick={handleDelete}>
          Delete task
        </button>
      </div>
      <ErrorBanner message={error} />

      <div className="detail-grid">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Description</h3>
          <p style={{ color: "var(--color-text-muted)", whiteSpace: "pre-wrap" }}>
            {task.description || "No description provided."}
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
                placeholder="Add a note..."
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
            <select value={task.status} onChange={(e) => updateField("status", e.target.value)}>
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s.replace("_", " ")}
                </option>
              ))}
            </select>
          </div>
          <div className="field-row">
            <span>Priority</span>
            <select value={task.priority} onChange={(e) => updateField("priority", e.target.value)}>
              {PRIORITY_OPTIONS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>
          <div className="field-row">
            <span>Assigned to</span>
            <select
              value={task.assigned_to_id || ""}
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
            <span>{userName(task.created_by_id)}</span>
          </div>
          <div className="field-row">
            <span>Created</span>
            <span>{new Date(task.created_at).toLocaleDateString()}</span>
          </div>
          <div className="field-row">
            <span>Updated</span>
            <span>{new Date(task.updated_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
