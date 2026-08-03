import apiClient from './apiClient';

export const rbacApi = {
  /**
   * GET /api/v1/rbac/roles/
   * List all platform roles and permissions
   */
  getRoles: () => {
    return apiClient.get('/api/v1/rbac/roles/');
  },

  /**
   * GET /api/v1/rbac/roles/:role/
   * Get detail for a specific platform role
   */
  getRoleDetail: (roleName) => {
    return apiClient.get(`/api/v1/rbac/roles/${encodeURIComponent(roleName)}/`);
  },

  /**
   * GET /api/v1/rbac/users/:id/roles/
   * Get assigned roles for user ID
   */
  getUserRoles: (userId) => {
    return apiClient.get(`/api/v1/rbac/users/${userId}/roles/`);
  },

  /**
   * GET /api/v1/rbac/users/:id/permissions/
   * Get aggregated permissions for user ID
   */
  getUserPermissions: (userId) => {
    return apiClient.get(`/api/v1/rbac/users/${userId}/permissions/`);
  },

  /**
   * POST /api/v1/rbac/users/:id/assign-role/
   * Assign a role to user ID
   */
  assignRole: (userId, role) => {
    return apiClient.post(`/api/v1/rbac/users/${userId}/assign-role/`, { role });
  },

  /**
   * POST /api/v1/rbac/users/:id/remove-role/
   * Remove a role from user ID
   */
  removeRole: (userId, role) => {
    return apiClient.post(`/api/v1/rbac/users/${userId}/remove-role/`, { role });
  },

  /**
   * PUT /api/v1/rbac/users/:id/replace-roles/
   * Replace all roles for user ID
   */
  replaceRoles: (userId, roles) => {
    return apiClient.put(`/api/v1/rbac/users/${userId}/replace-roles/`, { roles });
  },

  /**
   * DELETE /api/v1/rbac/users/:id/clear-roles/
   * Clear all assigned roles from user ID
   */
  clearRoles: (userId) => {
    return apiClient.delete(`/api/v1/rbac/users/${userId}/clear-roles/`);
  },
};

export default rbacApi;
