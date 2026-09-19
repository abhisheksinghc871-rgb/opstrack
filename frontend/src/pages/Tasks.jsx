import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { tasksApi, usersApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import ErrorBanner from "../components/ErrorBanner.jsx";
import Badge from "../components/Badge.jsx";

const STATUS_OPTIONS = ["todo", "in_progress", "blocked", "done"];
const PRIORITY_OPTIONS = ["low", "medium", "high", "critical"];

export default function Tasks() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [showForm, setShowForm] = useState(false);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (priorityFilter) params.priority = priorityFilter;
      const res = await tasksApi.list(params);
      setTasks(res.data);
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
    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, priorityFilter]);

  const userName = (id) => users.find((u) => u.id === id)?.full_name || "Unassigned";

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Tasks</h1>
        <button className="btn" onClick={() => setShowForm((v) => !v)}>
          {showForm ? "Cancel" : "New Task"}
        </button>
      </div>

      <ErrorBanner message={error} />

      {showForm && (
        <TaskForm
          users={users}
          onCreated={() => {
            setShowForm(false);
            loadTasks();
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
        <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
          <option value="">All priorities</option>
          {PRIORITY_OPTIONS.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>

      <div className="card" style={{ padding: 0 }}>
        {loading ? (
          <div className="loading-state">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">No tasks yet. Create the first one.</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Assigned to</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr
                  key={task.id}
                  className="clickable-row"
                  onClick={() => navigate(`/tasks/${task.id}`)}
                >
                  <td>{task.title}</td>
                  <td>
                    <Badge type="status" value={task.status} />
                  </td>
                  <td>
                    <Badge type="priority" value={task.priority} />
                  </td>
                  <td>{userName(task.assigned_to_id)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function TaskForm({ users, onCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [assignedTo, setAssignedTo] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await tasksApi.create({
        title,
        description,
        priority,
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
          <label>Priority</label>
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            {PRIORITY_OPTIONS.map((p) => (
              <option key={p} value={p}>
                {p}
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
          {submitting ? "Creating..." : "Create task"}
        </button>
      </form>
    </div>
  );
}
