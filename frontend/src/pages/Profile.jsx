import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) return null;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Profile</h1>
      </div>
      <div className="card" style={{ maxWidth: 420 }}>
        <div className="field-row">
          <span>Full name</span>
          <span>{user.full_name}</span>
        </div>
        <div className="field-row">
          <span>Email</span>
          <span>{user.email}</span>
        </div>
        <div className="field-row">
          <span>Account status</span>
          <span>{user.is_active ? "Active" : "Inactive"}</span>
        </div>
        <div className="field-row">
          <span>Member since</span>
          <span>{new Date(user.created_at).toLocaleDateString()}</span>
        </div>
        <button className="btn btn-danger" style={{ marginTop: 16 }} onClick={handleLogout}>
          Log out
        </button>
      </div>
    </div>
  );
}
