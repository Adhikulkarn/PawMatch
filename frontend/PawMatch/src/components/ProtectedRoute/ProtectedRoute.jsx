import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export const ProtectedRoute = ({ children, requiredRole = null, requiredPermission = null }) => {
  const { isAuthenticated, loading, hasRole, hasPermission } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div className="loading-spinner">Loading session...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && !hasRole(requiredRole)) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#e53e3e' }}>
        <h2>Access Denied</h2>
        <p>You do not have the required role ({Array.isArray(requiredRole) ? requiredRole.join(', ') : requiredRole}) to view this page.</p>
      </div>
    );
  }

  if (requiredPermission && !hasPermission(requiredPermission)) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#e53e3e' }}>
        <h2>Access Denied</h2>
        <p>You do not have the required permission ({Array.isArray(requiredPermission) ? requiredPermission.join(', ') : requiredPermission}) to view this page.</p>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;
