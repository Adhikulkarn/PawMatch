import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import authService from '../services/auth.service';

export const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [verifying, setVerifying] = useState(Boolean(token));
  const [status, setStatus] = useState({ success: null, message: '' });
  const [resendEmail, setResendEmail] = useState('');
  const [resending, setResending] = useState(false);
  const [resendStatus, setResendStatus] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      setVerifying(true);
      authService
        .verifyEmail(token, 'GET')
        .then((res) => {
          if (res.success) {
            setStatus({ success: true, message: res.message || 'Email verified successfully! You can now log in.' });
          } else {
            setStatus({ success: false, message: res.message || 'Email verification failed. The token may be invalid or expired.' });
          }
        })
        .catch((err) => {
          setStatus({ success: false, message: err.message || 'Verification error occurred.' });
        })
        .finally(() => setVerifying(false));
    }
  }, [token]);

  const handleResend = async (e) => {
    e.preventDefault();
    setResending(true);
    setResendStatus(null);
    try {
      const res = await authService.resendVerification(resendEmail);
      if (res.success) {
        setResendStatus({ success: true, message: res.message || 'Verification link sent to your email.' });
      } else {
        setResendStatus({ success: false, message: res.message || 'Failed to resend verification email.' });
      }
    } catch (err) {
      setResendStatus({ success: false, message: err.message });
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h2 className="heading-md" style={{ marginBottom: '0.5rem' }}>Email Verification</h2>
        </div>

        {verifying && (
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <div className="loading-spinner" style={{ width: '2rem', height: '2rem', borderColor: 'var(--color-accent-brown)' }}></div>
            <p style={{ marginTop: '1rem', color: 'var(--color-text-muted)' }}>Verifying your email token...</p>
          </div>
        )}

        {!verifying && status.success !== null && (
          <div>
            <div className={`alert ${status.success ? 'alert-success' : 'alert-error'}`}>
              {status.message}
            </div>
            {status.success && (
              <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
                <button className="btn-primary" onClick={() => navigate('/login')}>
                  Proceed to Login
                </button>
              </div>
            )}
          </div>
        )}

        {(!token || status.success === false) && !verifying && (
          <div style={{ marginTop: '2rem', borderTop: '1px solid var(--color-border)', paddingTop: '1.5rem' }}>
            <h4 style={{ fontSize: '1rem', marginBottom: '0.5rem', textAlign: 'center' }}>Resend Verification Link</h4>
            {resendStatus && (
              <div className={`alert ${resendStatus.success ? 'alert-success' : 'alert-error'}`}>
                {resendStatus.message}
              </div>
            )}
            <form onSubmit={handleResend}>
              <div className="form-group">
                <label className="form-label" htmlFor="resend-email">Your Email Address</label>
                <input
                  id="resend-email"
                  type="email"
                  className="form-input"
                  value={resendEmail}
                  onChange={(e) => setResendEmail(e.target.value)}
                  placeholder="user@example.com"
                  required
                  disabled={resending}
                />
              </div>
              <button type="submit" className="btn-secondary" disabled={resending} style={{ width: '100%', marginTop: '0.5rem' }}>
                {resending ? 'Sending...' : 'Resend Verification Email'}
              </button>
            </form>
          </div>
        )}

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.875rem' }}>
          <Link to="/login" style={{ color: 'var(--color-accent-brown)', fontWeight: '600' }}>
            ← Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmailPage;
