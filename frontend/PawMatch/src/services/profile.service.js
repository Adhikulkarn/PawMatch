import profileApi from '../api/profile.api';
import tokenStorage from '../utils/tokenStorage';

export const profileService = {
  getProfile: async () => {
    return profileApi.getProfile();
  },

  updateProfile: async (data) => {
    const res = await profileApi.updateProfile(data);
    if (res.success && res.data) {
      // Update cached user object if user data changed
      const currentUser = tokenStorage.getUser() || {};
      const updatedUser = {
        ...currentUser,
        first_name: res.data.first_name || currentUser.first_name,
        last_name: res.data.last_name || currentUser.last_name,
        phone_number: res.data.phone_number || currentUser.phone_number,
      };
      tokenStorage.setUser(updatedUser);
    }
    return res;
  },

  uploadAvatar: async (file) => {
    return profileApi.uploadAvatar(file);
  },

  deleteAvatar: async () => {
    return profileApi.deleteAvatar();
  },

  changePassword: async (payload) => {
    return profileApi.changePassword(payload);
  },

  deactivateAccount: async (password) => {
    const res = await profileApi.deactivateAccount(password);
    if (res.success) {
      tokenStorage.clear();
    }
    return res;
  },
};

export default profileService;
