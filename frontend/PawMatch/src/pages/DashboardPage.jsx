import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const DashboardPage = () => {
  const { user, userRoles, userPermissions, logout, hasRole } = useAuth();

  const isAdmin = hasRole('ADMINISTRATOR');

  return (
    <div className="container" style={{ padding: '3rem 1.5rem', maxWidth: '1000px' }}>
      {/* Header Banner */}
      <div
        className="auth-card"
        style={{
          maxWidth: '100%',
          marginBottom: '2rem',
          background: 'linear-gradient(135deg, var(--color-accent-brown-light) 0%, var(--color-bg-beige) 100%)',
          border: '1px solid var(--color-border)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <span className="badge badge-adopter" style={{ marginBottom: '0.5rem' }}>
              Logged In
            </span>
            <h1 className="heading-md">Welcome back, {user?.first_name || 'User'}!</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.95rem' }}>
              {user?.email} • Account status: Active
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <Link to="/profile" className="btn-secondary">
              Edit Profile
            </Link>
            {isAdmin && (
              <Link to="/admin/rbac" className="btn-primary" style={{ width: 'auto' }}>
                RBAC Management
              </Link>
            )}
            <button onClick={logout} className="btn-secondary" style={{ color: '#991b1b' }}>
              Sign Out
            </button>
          </div>
        </div>
      </div>

      {/* Grid Content */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
        {/* Roles & Permissions Card */}
        <div className="auth-card" style={{ maxWidth: '100%' }}>
          <h3 className="heading-sm" style={{ marginBottom: '1rem' }}>Assigned Roles & Security</h3>
          <div style={{ marginBottom: '1.25rem' }}>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
              Platform Roles
            </h4>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {userRoles.length > 0 ? (
                userRoles.map((role) => (
                  <span key={role} className="badge badge-shelter">
                    {role}
                  </span>
                ))
              ) : (
                <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>No explicit roles assigned</span>
              )}
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
              Granted Permissions ({userPermissions.length})
            </h4>
            <div style={{ maxHeight: '180px', overflowY: 'auto', padding: '0.5rem', background: 'var(--color-bg-cream)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
              {userPermissions.length > 0 ? (
                <ul style={{ listStyle: 'none', fontSize: '0.8rem', paddingLeft: 0 }}>
                  {userPermissions.map((perm) => (
                    <li key={perm} style={{ padding: '0.2rem 0', borderBottom: '1px solid rgba(0,0,0,0.04)' }}>
                      ✓ {perm}
                    </li>
                  ))}
                </ul>
              ) : (
                <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Standard adopter default access</span>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions Card */}
        <div className="auth-card" style={{ maxWidth: '100%' }}>
          <h3 className="heading-sm" style={{ marginBottom: '1rem' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <Link to="/#adopt" className="btn-secondary" style={{ textAlign: 'center' }}>
              🐾 Explore Pet Catalog
            </Link>
            <Link to="/profile" className="btn-secondary" style={{ textAlign: 'center' }}>
              👤 Update Account Details
            </Link>
            {isAdmin && (
              <Link to="/admin/rbac" className="btn-secondary" style={{ textAlign: 'center', borderColor: 'var(--color-accent-brown)' }}>
                🛡️ Manage User RBAC Roles
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
