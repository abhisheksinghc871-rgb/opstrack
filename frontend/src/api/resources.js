import apiClient from "./client";

export const authApi = {
  login: (email, password) => apiClient.post("/api/auth/login", { email, password }),
  register: (email, fullName, password) =>
    apiClient.post("/api/auth/register", { email, full_name: fullName, password }),
  me: () => apiClient.get("/api/auth/me"),
};

export const usersApi = {
  list: () => apiClient.get("/api/users"),
};

export const tasksApi = {
  list: (params = {}) => apiClient.get("/api/tasks", { params }),
  get: (id) => apiClient.get(`/api/tasks/${id}`),
  create: (payload) => apiClient.post("/api/tasks", payload),
  update: (id, payload) => apiClient.patch(`/api/tasks/${id}`, payload),
  remove: (id) => apiClient.delete(`/api/tasks/${id}`),
};

export const incidentsApi = {
  list: (params = {}) => apiClient.get("/api/incidents", { params }),
  get: (id) => apiClient.get(`/api/incidents/${id}`),
  create: (payload) => apiClient.post("/api/incidents", payload),
  update: (id, payload) => apiClient.patch(`/api/incidents/${id}`, payload),
  remove: (id) => apiClient.delete(`/api/incidents/${id}`),
};

export const commentsApi = {
  list: (entityType, entityId) =>
    apiClient.get("/api/comments", { params: { entity_type: entityType, entity_id: entityId } }),
  create: (entityType, entityId, body) =>
    apiClient.post("/api/comments", { entity_type: entityType, entity_id: entityId, body }),
  remove: (id) => apiClient.delete(`/api/comments/${id}`),
};

export const dashboardApi = {
  stats: () => apiClient.get("/api/dashboard/stats"),
};
