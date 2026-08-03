import React, { useState, useEffect } from 'react';
import useProfile from '../hooks/useProfile';
import { useAuth } from '../contexts/AuthContext';

export const ProfilePage = () => {
  const {
    profile,
    loading: profileLoading,
    error: profileError,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
    changePassword,
    deactivateAccount,
  } = useProfile();

  const { userRoles } = useAuth();

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
    bio: '',
    date_of_birth: '',
  });

  const [pwData, setPwData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  const [deactivatePw, setDeactivatePw] = useState('');

  const [submittingProfile, setSubmittingProfile] = useState(false);
  const [submittingAvatar, setSubmittingAvatar] = useState(false);
  const [submittingPw, setSubmittingPw] = useState(false);
  const [submittingDeactivate, setSubmittingDeactivate] = useState(false);

  const [profileAlert, setProfileAlert] = useState(null);
  const [pwAlert, setPwAlert] = useState(null);
  const [avatarAlert, setAvatarAlert] = useState(null);
  const [deactivateAlert, setDeactivateAlert] = useState(null);

  useEffect(() => {
    if (profile) {
      setFormData({
        first_name: profile.first_name || '',
        last_name: profile.last_name || '',
        phone_number: profile.phone_number || '',
        bio: profile.bio || '',
        date_of_birth: profile.date_of_birth || '',
      });
    }
  }, [profile]);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setSubmittingProfile(true);
    setProfileAlert(null);
    try {
      const res = await updateProfile(formData);
      if (res.success) {
        setProfileAlert({ type: 'success', text: res.message || 'Profile updated successfully!' });
      } else {
        setProfileAlert({ type: 'error', text: res.message || 'Profile update failed.' });
      }
    } catch (err) {
      setProfileAlert({ type: 'error', text: err.message || 'Update failed.' });
    } finally {
      setSubmittingProfile(false);
    }
  };

  const handleAvatarChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setSubmittingAvatar(true);
    setAvatarAlert(null);
    try {
      const res = await uploadAvatar(file);
      if (res.success) {
        setAvatarAlert({ type: 'success', text: res.message || 'Avatar uploaded successfully!' });
      } else {
        setAvatarAlert({ type: 'error', text: res.message || 'Avatar upload failed.' });
      }
    } catch (err) {
      setAvatarAlert({ type: 'error', text: err.message || 'Avatar upload failed.' });
    } finally {
      setSubmittingAvatar(false);
    }
  };

  const handleAvatarDelete = async () => {
    setSubmittingAvatar(true);
    setAvatarAlert(null);
    try {
      const res = await deleteAvatar();
      if (res.success) {
        setAvatarAlert({ type: 'success', text: res.message || 'Avatar removed successfully!' });
      } else {
        setAvatarAlert({ type: 'error', text: res.message || 'Failed to remove avatar.' });
      }
    } catch (err) {
      setAvatarAlert({ type: 'error', text: err.message });
    } finally {
      setSubmittingAvatar(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setPwAlert(null);

    if (pwData.new_password !== pwData.confirm_password) {
      setPwAlert({ type: 'error', text: 'New passwords do not match.' });
      return;
    }

    setSubmittingPw(true);
    try {
      const res = await changePassword(pwData);
      if (res.success) {
        setPwAlert({ type: 'success', text: res.message || 'Password changed successfully!' });
        setPwData({ current_password: '', new_password: '', confirm_password: '' });
      } else {
        setPwAlert({ type: 'error', text: res.message || 'Failed to change password.' });
      }
    } catch (err) {
      setPwAlert({ type: 'error', text: err.message });
    } finally {
      setSubmittingPw(false);
    }
  };

  const handleDeactivate = async (e) => {
    e.preventDefault();
    if (!window.confirm('Are you sure you want to deactivate your PawMatch account? This action cannot be undone.')) {
      return;
    }

    setSubmittingDeactivate(true);
    setDeactivateAlert(null);
    try {
      const res = await deactivateAccount(deactivatePw);
      if (res.success) {
        window.location.href = '/login';
      } else {
        setDeactivateAlert({ type: 'error', text: res.message || 'Deactivation failed.' });
      }
    } catch (err) {
      setDeactivateAlert({ type: 'error', text: err.message });
    } finally {
      setSubmittingDeactivate(false);
    }
  };

  if (profileLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div className="loading-spinner" style={{ borderColor: 'var(--color-accent-brown)' }}></div>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: '3rem 1.5rem', maxWidth: '840px' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 className="heading-lg">User Profile</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Manage your personal details and account security settings</p>
      </div>

      {profileError && <div className="alert alert-error">{profileError}</div>}

      {/* Profile Overview & Avatar Card */}
      <div className="auth-card" style={{ maxWidth: '100%', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative' }}>
            {profile?.avatar ? (
              <img
                src={profile.avatar}
                alt="User Avatar"
                style={{ width: '96px', height: '96px', borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--color-accent-brown)' }}
              />
            ) : (
              <div
                style={{
                  width: '96px',
                  height: '96px',
                  borderRadius: '50%',
                  backgroundColor: 'var(--color-accent-brown-light)',
                  color: 'var(--color-accent-brown)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem',
                  fontWeight: 'bold',
                }}
              >
                {profile?.first_name ? profile.first_name[0].toUpperCase() : 'U'}
              </div>
            )}
          </div>

          <div style={{ flex: 1 }}>
            <h3 className="heading-sm">{profile?.first_name} {profile?.last_name}</h3>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>{profile?.email}</p>
            <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {userRoles.map((r) => (
                <span key={r} className="badge badge-adopter">
                  {r}
                </span>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label className="btn-secondary" style={{ cursor: 'pointer', textAlign: 'center' }}>
              {submittingAvatar ? 'Uploading...' : 'Change Avatar'}
              <input type="file" accept="image/*" onChange={handleAvatarChange} style={{ display: 'none' }} disabled={submittingAvatar} />
            </label>
            {profile?.avatar && (
              <button onClick={handleAvatarDelete} className="btn-secondary" style={{ color: '#dc2626' }} disabled={submittingAvatar}>
                Remove Avatar
              </button>
            )}
          </div>
        </div>

        {avatarAlert && <div className={`alert alert-${avatarAlert.type}`} style={{ marginTop: '1rem' }}>{avatarAlert.text}</div>}
      </div>

      {/* Edit Profile Form */}
      <div className="auth-card" style={{ maxWidth: '100%', marginBottom: '2rem' }}>
        <h3 className="heading-sm" style={{ marginBottom: '1.25rem' }}>Personal Information</h3>

        {profileAlert && <div className={`alert alert-${profileAlert.type}`}>{profileAlert.text}</div>}

        <form onSubmit={handleProfileSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">First Name</label>
              <input
                type="text"
                className="form-input"
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                disabled={submittingProfile}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Last Name</label>
              <input
                type="text"
                className="form-input"
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                disabled={submittingProfile}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Phone Number</label>
            <input
              type="text"
              className="form-input"
              value={formData.phone_number}
              onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
              placeholder="+1 555-0199"
              disabled={submittingProfile}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Date of Birth</label>
            <input
              type="date"
              className="form-input"
              value={formData.date_of_birth}
              onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
              disabled={submittingProfile}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Bio / Adoption Notes</label>
            <textarea
              className="form-input"
              rows="3"
              value={formData.bio}
              onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              placeholder="Tell shelters a little bit about yourself..."
              disabled={submittingProfile}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={submittingProfile} style={{ marginTop: '0.5rem' }}>
            {submittingProfile ? 'Saving...' : 'Save Profile Changes'}
          </button>
        </form>
      </div>

      {/* Change Password Form */}
      <div className="auth-card" style={{ maxWidth: '100%', marginBottom: '2rem' }}>
        <h3 className="heading-sm" style={{ marginBottom: '1.25rem' }}>Change Password</h3>

        {pwAlert && <div className={`alert alert-${pwAlert.type}`}>{pwAlert.text}</div>}

        <form onSubmit={handleChangePassword}>
          <div className="form-group">
            <label className="form-label">Current Password</label>
            <input
              type="password"
              className="form-input"
              value={pwData.current_password}
              onChange={(e) => setPwData({ ...pwData, current_password: e.target.value })}
              required
              disabled={submittingPw}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">New Password</label>
              <input
                type="password"
                className="form-input"
                value={pwData.new_password}
                onChange={(e) => setPwData({ ...pwData, new_password: e.target.value })}
                required
                disabled={submittingPw}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm New Password</label>
              <input
                type="password"
                className="form-input"
                value={pwData.confirm_password}
                onChange={(e) => setPwData({ ...pwData, confirm_password: e.target.value })}
                required
                disabled={submittingPw}
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={submittingPw} style={{ marginTop: '0.5rem' }}>
            {submittingPw ? 'Updating Password...' : 'Update Password'}
          </button>
        </form>
      </div>

      {/* Deactivate Account */}
      <div className="auth-card" style={{ maxWidth: '100%', borderColor: '#fca5a5' }}>
        <h3 className="heading-sm" style={{ color: '#dc2626', marginBottom: '0.5rem' }}>Deactivate Account</h3>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '1rem' }}>
          Deactivating your account will disable your access and archive your data in compliance with system policies.
        </p>

        {deactivateAlert && <div className={`alert alert-${deactivateAlert.type}`}>{deactivateAlert.text}</div>}

        <form onSubmit={handleDeactivate}>
          <div className="form-group">
            <label className="form-label">Confirm Password to Deactivate</label>
            <input
              type="password"
              className="form-input"
              value={deactivatePw}
              onChange={(e) => setDeactivatePw(e.target.value)}
              required
              disabled={submittingDeactivate}
            />
          </div>
          <button type="submit" className="btn-secondary" style={{ backgroundColor: '#fee2e2', color: '#991b1b', border: '1px solid #fca5a5', width: '100%' }} disabled={submittingDeactivate}>
            {submittingDeactivate ? 'Deactivating...' : 'Deactivate Account'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;
