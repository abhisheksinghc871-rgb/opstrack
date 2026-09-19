import apiClient from "./client";

export const authApi = {
  login: (email, password) => apiClient.post("/auth/login", { email, password }),
  register: (email, fullName, password) =>
    apiClient.post("/auth/register", { email, full_name: fullName, password }),
  me: () => apiClient.get("/auth/me"),
};

export const usersApi = {
  list: () => apiClient.get("/users"),
};

export const tasksApi = {
  list: (params = {}) => apiClient.get("/tasks", { params }),
  get: (id) => apiClient.get(`/tasks/${id}`),
  create: (payload) => apiClient.post("/tasks", payload),
  update: (id, payload) => apiClient.patch(`/tasks/${id}`, payload),
  remove: (id) => apiClient.delete(`/tasks/${id}`),
};

export const incidentsApi = {
  list: (params = {}) => apiClient.get("/incidents", { params }),
  get: (id) => apiClient.get(`/incidents/${id}`),
  create: (payload) => apiClient.post("/incidents", payload),
  update: (id, payload) => apiClient.patch(`/incidents/${id}`, payload),
  remove: (id) => apiClient.delete(`/incidents/${id}`),
};

export const commentsApi = {
  list: (entityType, entityId) =>
    apiClient.get("/comments", { params: { entity_type: entityType, entity_id: entityId } }),
  create: (entityType, entityId, body) =>
    apiClient.post("/comments", { entity_type: entityType, entity_id: entityId, body }),
  remove: (id) => apiClient.delete(`/comments/${id}`),
};

export const dashboardApi = {
  stats: () => apiClient.get("/dashboard/stats"),
};
