import { useState, useCallback } from 'react';
import rbacService from '../services/rbac.service';
import { useAuth } from '../contexts/AuthContext';

export const useRBAC = () => {
  const { userRoles, userPermissions, hasRole, hasPermission } = useAuth();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAllRoles = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await rbacService.getRoles();
      if (res.success) {
        setRoles(res.data);
      } else {
        setError(res.message);
      }
      return res;
    } catch (err) {
      setError(err.message || 'Failed to fetch roles.');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchUserRoles = async (userId) => {
    return rbacService.getUserRoles(userId);
  };

  const fetchUserPermissions = async (userId) => {
    return rbacService.getUserPermissions(userId);
  };

  const assignRole = async (userId, role) => {
    return rbacService.assignRole(userId, role);
  };

  const removeRole = async (userId, role) => {
    return rbacService.removeRole(userId, role);
  };

  const replaceRoles = async (userId, rolesList) => {
    return rbacService.replaceRoles(userId, rolesList);
  };

  const clearRoles = async (userId) => {
    return rbacService.clearRoles(userId);
  };

  return {
    userRoles,
    userPermissions,
    hasRole,
    hasPermission,
    roles,
    loading,
    error,
    fetchAllRoles,
    fetchUserRoles,
    fetchUserPermissions,
    assignRole,
    removeRole,
    replaceRoles,
    clearRoles,
  };
};

export default useRBAC;
