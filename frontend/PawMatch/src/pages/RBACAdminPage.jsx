import React, { useState, useEffect } from 'react';
import useRBAC from '../hooks/useRBAC';

export const RBACAdminPage = () => {
  const {
    roles,
    loading: rolesLoading,
    error: rolesError,
    fetchAllRoles,
    fetchUserRoles,
    fetchUserPermissions,
    assignRole,
    removeRole,
    replaceRoles,
    clearRoles,
  } = useRBAC();

  const [selectedUserId, setSelectedUserId] = useState('');
  const [targetUserRoles, setTargetUserRoles] = useState([]);
  const [targetUserPermissions, setTargetUserPermissions] = useState([]);
  const [loadingUserRBAC, setLoadingUserRBAC] = useState(false);

  const [roleToAssign, setRoleToAssign] = useState('');
  const [roleToRemove, setRoleToRemove] = useState('');
  const [replaceRolesInput, setReplaceRolesInput] = useState('');

  const [actionAlert, setActionAlert] = useState(null);

  useEffect(() => {
    fetchAllRoles();
  }, [fetchAllRoles]);

  const handleInspectUser = async (e) => {
    e.preventDefault();
    if (!selectedUserId) return;

    setLoadingUserRBAC(true);
    setActionAlert(null);
    try {
      const [rolesRes, permsRes] = await Promise.all([
        fetchUserRoles(selectedUserId),
        fetchUserPermissions(selectedUserId),
      ]);

      if (rolesRes.success) {
        setTargetUserRoles(rolesRes.data?.roles || []);
      }
      if (permsRes.success) {
        setTargetUserPermissions(permsRes.data?.permissions || []);
      }
    } catch (err) {
      setActionAlert({ type: 'error', text: err.message || 'Failed to fetch user RBAC data.' });
    } finally {
      setLoadingUserRBAC(false);
    }
  };

  const handleAssignRole = async (e) => {
    e.preventDefault();
    if (!selectedUserId || !roleToAssign) return;
    setActionAlert(null);
    try {
      const res = await assignRole(selectedUserId, roleToAssign);
      if (res.success) {
        setActionAlert({ type: 'success', text: res.message || `Role ${roleToAssign} assigned.` });
        handleInspectUser(e);
      } else {
        setActionAlert({ type: 'error', text: res.message || 'Assign role failed.' });
      }
    } catch (err) {
      setActionAlert({ type: 'error', text: err.message });
    }
  };

  const handleRemoveRole = async (e) => {
    e.preventDefault();
    if (!selectedUserId || !roleToRemove) return;
    setActionAlert(null);
    try {
      const res = await removeRole(selectedUserId, roleToRemove);
      if (res.success) {
        setActionAlert({ type: 'success', text: res.message || `Role ${roleToRemove} removed.` });
        handleInspectUser(e);
      } else {
        setActionAlert({ type: 'error', text: res.message || 'Remove role failed.' });
      }
    } catch (err) {
      setActionAlert({ type: 'error', text: err.message });
    }
  };

  const handleReplaceRoles = async (e) => {
    e.preventDefault();
    if (!selectedUserId) return;
    setActionAlert(null);
    const newRolesList = replaceRolesInput
      .split(',')
      .map((r) => r.trim().toUpperCase())
      .filter(Boolean);

    try {
      const res = await replaceRoles(selectedUserId, newRolesList);
      if (res.success) {
        setActionAlert({ type: 'success', text: res.message || 'User roles replaced successfully.' });
        handleInspectUser(e);
      } else {
        setActionAlert({ type: 'error', text: res.message });
      }
    } catch (err) {
      setActionAlert({ type: 'error', text: err.message });
    }
  };

  const handleClearRoles = async () => {
    if (!selectedUserId) return;
    if (!window.confirm('Clear all roles from target user?')) return;
    setActionAlert(null);
    try {
      const res = await clearRoles(selectedUserId);
      if (res.success) {
        setActionAlert({ type: 'success', text: res.message || 'All user roles cleared.' });
        handleInspectUser({ preventDefault: () => {} });
      } else {
        setActionAlert({ type: 'error', text: res.message });
      }
    } catch (err) {
      setActionAlert({ type: 'error', text: err.message });
    }
  };

  return (
    <div className="container" style={{ padding: '3rem 1.5rem', maxWidth: '1000px' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 className="heading-lg">RBAC Management Console</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>
          Manage system roles, assign user permissions, and enforce security policies
        </p>
      </div>

      {rolesError && <div className="alert alert-error">{rolesError}</div>}

      {/* System Defined Roles Grid */}
      <div className="auth-card" style={{ maxWidth: '100%', marginBottom: '2rem' }}>
        <h3 className="heading-sm" style={{ marginBottom: '1rem' }}>Platform Defined Roles</h3>
        {rolesLoading ? (
          <p>Loading roles definition...</p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {roles.map((r) => (
              <div key={r.role} style={{ padding: '1rem', background: 'var(--color-bg-cream)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="badge badge-admin">{r.role}</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{r.permission_count} perms</span>
                </div>
                <h4 style={{ fontSize: '0.95rem', marginTop: '0.5rem' }}>{r.display_name}</h4>
                <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--color-text-muted)', maxHeight: '60px', overflowY: 'auto' }}>
                  {r.permissions.join(', ')}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* User Role Management Operations */}
      <div className="auth-card" style={{ maxWidth: '100%' }}>
        <h3 className="heading-sm" style={{ marginBottom: '1.25rem' }}>User Role Management</h3>

        <form onSubmit={handleInspectUser} style={{ marginBottom: '1.5rem' }}>
          <div className="form-group">
            <label className="form-label">Target User UUID</label>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <input
                type="text"
                className="form-input"
                value={selectedUserId}
                onChange={(e) => setSelectedUserId(e.target.value)}
                placeholder="e.g. 123e4567-e89b-12d3-a456-426614174000"
                required
              />
              <button type="submit" className="btn-primary" style={{ width: 'auto', whiteSpace: 'nowrap' }}>
                Inspect User
              </button>
            </div>
          </div>
        </form>

        {actionAlert && <div className={`alert alert-${actionAlert.type}`}>{actionAlert.text}</div>}

        {loadingUserRBAC ? (
          <p>Loading user RBAC state...</p>
        ) : selectedUserId ? (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            {/* Left Column: Current State */}
            <div style={{ padding: '1rem', background: 'var(--color-bg-cream)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
              <h4 style={{ marginBottom: '0.75rem' }}>Assigned Roles</h4>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                {targetUserRoles.length > 0 ? (
                  targetUserRoles.map((r) => (
                    <span key={r} className="badge badge-shelter">
                      {r}
                    </span>
                  ))
                ) : (
                  <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>No explicit roles assigned</span>
                )}
              </div>

              <h4 style={{ marginBottom: '0.5rem' }}>Permissions ({targetUserPermissions.length})</h4>
              <div style={{ maxHeight: '150px', overflowY: 'auto', fontSize: '0.8rem' }}>
                {targetUserPermissions.map((p) => (
                  <div key={p}>• {p}</div>
                ))}
              </div>
            </div>

            {/* Right Column: Actions */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Assign Role */}
              <form onSubmit={handleAssignRole} style={{ display: 'flex', gap: '0.5rem' }}>
                <select className="form-input" value={roleToAssign} onChange={(e) => setRoleToAssign(e.target.value)} required>
                  <option value="">Select Role to Assign</option>
                  {roles.map((r) => (
                    <option key={r.role} value={r.role}>{r.role} ({r.display_name})</option>
                  ))}
                </select>
                <button type="submit" className="btn-secondary" style={{ whiteSpace: 'nowrap' }}>Assign</button>
              </form>

              {/* Remove Role */}
              <form onSubmit={handleRemoveRole} style={{ display: 'flex', gap: '0.5rem' }}>
                <select className="form-input" value={roleToRemove} onChange={(e) => setRoleToRemove(e.target.value)} required>
                  <option value="">Select Role to Remove</option>
                  {targetUserRoles.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
                <button type="submit" className="btn-secondary" style={{ whiteSpace: 'nowrap', color: '#dc2626' }}>Remove</button>
              </form>

              {/* Replace Roles */}
              <form onSubmit={handleReplaceRoles}>
                <div className="form-group" style={{ marginBottom: '0.5rem' }}>
                  <input
                    type="text"
                    className="form-input"
                    value={replaceRolesInput}
                    onChange={(e) => setReplaceRolesInput(e.target.value)}
                    placeholder="Comma-separated roles (e.g. ADOPTER, VOLUNTEER)"
                  />
                </div>
                <button type="submit" className="btn-secondary" style={{ width: '100%' }}>Replace All Roles</button>
              </form>

              {/* Clear Roles */}
              <button onClick={handleClearRoles} className="btn-secondary" style={{ backgroundColor: '#fee2e2', color: '#991b1b', border: '1px solid #fca5a5' }}>
                Clear All Roles
              </button>
            </div>
          </div>
        ) : (
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Enter a User ID above to inspect and modify role assignments.</p>
        )}
      </div>
    </div>
  );
};

export default RBACAdminPage;
