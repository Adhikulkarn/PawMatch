export const handleApiResponse = (response) => {
  const data = response?.data;

  // Handles standard PawMatch API structure: { success, message, data, errors }
  if (data && typeof data === 'object' && 'success' in data) {
    return {
      success: data.success,
      message: data.message || '',
      data: data.data !== undefined ? data.data : null,
      errors: data.errors || null,
      status: response.status,
    };
  }

  // Fallback for standard REST endpoints returning raw JSON
  return {
    success: response.status >= 200 && response.status < 300,
    message: response.statusText || 'Operation completed successfully.',
    data: data || null,
    errors: null,
    status: response.status,
  };
};

export default handleApiResponse;
