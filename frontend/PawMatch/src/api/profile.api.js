import apiClient from './apiClient';

export const profileApi = {
  /**
   * GET /api/v1/accounts/me/
   * Get authenticated user basic account details
   */
  getCurrentUser: () => {
    return apiClient.get('/api/v1/accounts/me/');
  },

  /**
   * GET /api/v1/accounts/profile/
   * Get full authenticated user profile details
   */
  getProfile: () => {
    return apiClient.get('/api/v1/accounts/profile/');
  },

  /**
   * PATCH /api/v1/accounts/profile/
   * Update profile fields (first_name, last_name, phone_number, bio, date_of_birth, preferences)
   */
  updateProfile: (profileData) => {
    return apiClient.patch('/api/v1/accounts/profile/', profileData);
  },

  /**
   * POST /api/v1/accounts/profile/avatar/
   * Upload user profile avatar image (Multipart form-data)
   */
  uploadAvatar: (file) => {
    const formData = new FormData();
    formData.append('avatar', file);
    return apiClient.post('/api/v1/accounts/profile/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * DELETE /api/v1/accounts/profile/avatar/
   * Remove current user avatar image
   */
  deleteAvatar: () => {
    return apiClient.delete('/api/v1/accounts/profile/avatar/');
  },

  /**
   * POST /api/v1/accounts/change-password/
   * Change user password with current password verification
   */
  changePassword: (payload) => {
    return apiClient.post('/api/v1/accounts/change-password/', payload);
  },

  /**
   * POST /api/v1/accounts/deactivate/
   * Deactivate user account with password confirmation
   */
  deactivateAccount: (password) => {
    return apiClient.post('/api/v1/accounts/deactivate/', { password });
  },
};

export default profileApi;
