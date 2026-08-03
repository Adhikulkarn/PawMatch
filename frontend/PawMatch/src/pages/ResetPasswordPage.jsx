import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import authService from '../services/auth.service';

export const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const tokenFromUrl = searchParams.get('token') || '';

  const [token, setToken] = useState(tokenFromUrl);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, [tokenFromUrl]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setErrorMsg('');

    if (newPassword !== confirmPassword) {
      setErrorMsg('Passwords do not match.');
      return;
    }

    setSubmitting(true);

    try {
      const res = await authService.resetPassword({
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });

      if (res.success) {
        setMessage(res.message || 'Password reset successfully! Redirecting to login...');
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        setErrorMsg(res.message || 'Failed to reset password.');
      }
    } catch (err) {
      setErrorMsg(err.message || 'An error occurred while resetting password.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h2 className="heading-md" style={{ marginBottom: '0.5rem' }}>Reset Password</h2>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
            Set a new secure password for your PawMatch account
          </p>
        </div>

        {errorMsg && <div className="alert alert-error">{errorMsg}</div>}
        {message && <div className="alert alert-success">{message}</div>}

        <form onSubmit={handleSubmit}>
          {!tokenFromUrl && (
            <div className="form-group">
              <label className="form-label" htmlFor="reset-token">Reset Token</label>
              <input
                id="reset-token"
                type="text"
                className="form-input"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                required
                disabled={submitting}
              />
            </div>
          )}

          <div className="form-group">
            <label className="form-label" htmlFor="reset-new-password">New Password</label>
            <input
              id="reset-new-password"
              type="password"
              className="form-input"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={submitting}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="reset-confirm-password">Confirm New Password</label>
            <input
              id="reset-confirm-password"
              type="password"
              className="form-input"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={submitting}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={submitting} style={{ marginTop: '1rem' }}>
            {submitting ? <span className="loading-spinner"></span> : 'Reset Password'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.875rem' }}>
          <Link to="/login" style={{ color: 'var(--color-accent-brown)', fontWeight: '600' }}>
            ← Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage;
