import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import authService from '../services/auth.service';

export const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setErrorMsg('');
    setSubmitting(true);

    try {
      const res = await authService.forgotPassword(email);
      if (res.success) {
        setMessage(res.message || 'If an account exists with this email, a password reset link has been sent.');
      } else {
        setErrorMsg(res.message || 'Failed to request password reset.');
      }
    } catch (err) {
      setErrorMsg(err.message || 'An error occurred.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h2 className="heading-md" style={{ marginBottom: '0.5rem' }}>Forgot Password</h2>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
            Enter your account email to receive a password reset link
          </p>
        </div>

        {errorMsg && <div className="alert alert-error">{errorMsg}</div>}
        {message && <div className="alert alert-success">{message}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="forgot-email">Email Address</label>
            <input
              id="forgot-email"
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
              required
              disabled={submitting}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={submitting} style={{ marginTop: '1rem' }}>
            {submitting ? <span className="loading-spinner"></span> : 'Send Reset Link'}
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

export default ForgotPasswordPage;
