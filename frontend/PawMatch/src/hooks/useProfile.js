import { useState, useEffect, useCallback } from 'react';
import profileService from '../services/profile.service';
import { useAuth } from '../contexts/AuthContext';

export const useProfile = () => {
  const { user, loadUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await profileService.getProfile();
      if (res.success) {
        setProfile(res.data);
      } else {
        setError(res.message || 'Failed to fetch profile.');
      }
    } catch (err) {
      setError(err.message || 'Error fetching profile.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user, fetchProfile]);

  const updateProfile = async (data) => {
    setLoading(true);
    try {
      const res = await profileService.updateProfile(data);
      if (res.success) {
        setProfile(res.data);
        await loadUser();
      }
      return res;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const uploadAvatar = async (file) => {
    setLoading(true);
    try {
      const res = await profileService.uploadAvatar(file);
      if (res.success) {
        await fetchProfile();
        await loadUser();
      }
      return res;
    } finally {
      setLoading(false);
    }
  };

  const deleteAvatar = async () => {
    setLoading(true);
    try {
      const res = await profileService.deleteAvatar();
      if (res.success) {
        await fetchProfile();
        await loadUser();
      }
      return res;
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async (payload) => {
    return profileService.changePassword(payload);
  };

  const deactivateAccount = async (password) => {
    return profileService.deactivateAccount(password);
  };

  return {
    profile,
    loading,
    error,
    refetchProfile: fetchProfile,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
    changePassword,
    deactivateAccount,
  };
};

export default useProfile;
