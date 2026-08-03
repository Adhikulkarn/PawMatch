import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});
  const [successMsg, setSuccessMsg] = useState('');

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (fieldErrors[e.target.name]) {
      setFieldErrors({ ...fieldErrors, [e.target.name]: null });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setFieldErrors({});
    setSuccessMsg('');

    if (formData.password !== formData.confirm_password) {
      setErrorMsg('Passwords do not match.');
      return;
    }

    setSubmitting(true);

    try {
      const res = await register(formData);
      if (res.success) {
        setSuccessMsg(res.message || 'Registration successful! Please check your email to verify your account.');
        setTimeout(() => {
          navigate('/login');
        }, 2500);
      } else {
        setErrorMsg(res.message || 'Registration failed.');
        if (res.errors) {
          setFieldErrors(res.errors);
        }
      }
    } catch (err) {
      setErrorMsg(err.message || 'Registration error occurred.');
      if (err.errors) {
        setFieldErrors(err.errors);
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h2 className="heading-md" style={{ marginBottom: '0.5rem' }}>Create Account</h2>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
            Join PawMatch to start your pet adoption journey
          </p>
        </div>

        {errorMsg && <div className="alert alert-error">{errorMsg}</div>}
        {successMsg && <div className="alert alert-success">{successMsg}</div>}

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="register-first-name">First Name</label>
              <input
                id="register-first-name"
                name="first_name"
                type="text"
                className="form-input"
                value={formData.first_name}
                onChange={handleChange}
                required
                disabled={submitting}
              />
              {fieldErrors.first_name && <span style={{ color: '#dc2626', fontSize: '0.75rem' }}>{fieldErrors.first_name[0]}</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="register-last-name">Last Name</label>
              <input
                id="register-last-name"
                name="last_name"
                type="text"
                className="form-input"
                value={formData.last_name}
                onChange={handleChange}
                required
                disabled={submitting}
              />
              {fieldErrors.last_name && <span style={{ color: '#dc2626', fontSize: '0.75rem' }}>{fieldErrors.last_name[0]}</span>}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="register-email">Email Address</label>
            <input
              id="register-email"
              name="email"
              type="email"
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              placeholder="user@example.com"
              required
              disabled={submitting}
            />
            {fieldErrors.email && <span style={{ color: '#dc2626', fontSize: '0.75rem' }}>{fieldErrors.email[0]}</span>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="register-password">Password</label>
            <input
              id="register-password"
              name="password"
              type="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
              disabled={submitting}
            />
            {fieldErrors.password && <span style={{ color: '#dc2626', fontSize: '0.75rem' }}>{fieldErrors.password[0]}</span>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="register-confirm-password">Confirm Password</label>
            <input
              id="register-confirm-password"
              name="confirm_password"
              type="password"
              className="form-input"
              value={formData.confirm_password}
              onChange={handleChange}
              placeholder="••••••••"
              required
              disabled={submitting}
            />
            {fieldErrors.confirm_password && <span style={{ color: '#dc2626', fontSize: '0.75rem' }}>{fieldErrors.confirm_password[0]}</span>}
          </div>

          <button type="submit" className="btn-primary" disabled={submitting} style={{ marginTop: '1rem' }}>
            {submitting ? <span className="loading-spinner"></span> : 'Register'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--color-accent-brown)', fontWeight: '600' }}>
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
