import rbacApi from '../api/rbac.api';

export const rbacService = {
  getRoles: () => rbacApi.getRoles(),
  getRoleDetail: (role) => rbacApi.getRoleDetail(role),
  getUserRoles: (userId) => rbacApi.getUserRoles(userId),
  getUserPermissions: (userId) => rbacApi.getUserPermissions(userId),
  assignRole: (userId, role) => rbacApi.assignRole(userId, role),
  removeRole: (userId, role) => rbacApi.removeRole(userId, role),
  replaceRoles: (userId, roles) => rbacApi.replaceRoles(userId, roles),
  clearRoles: (userId) => rbacApi.clearRoles(userId),
};

export default rbacService;
