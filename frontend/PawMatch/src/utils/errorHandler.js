function getStatusFallbackMessage(status) {
  switch (status) {
    case 400:
      return 'Bad request. Please verify your submitted data.';
    case 401:
      return 'Authentication credentials invalid or expired. Please login again.';
    case 403:
      return 'Permission denied. You do not have access to this resource.';
    case 404:
      return 'The requested resource was not found.';
    case 422:
      return 'Validation failed for submitted data.';
    case 500:
      return 'Internal server error. Please try again later.';
    default:
      return 'An unexpected error occurred.';
  }
}

export const parseApiError = (error) => {
  if (error.response) {
    const status = error.response.status;
    const data = error.response.data;

    let message = getStatusFallbackMessage(status);
    let errors = null;

    if (data && typeof data === 'object') {
      message = data.message || data.detail || message;
      errors = data.errors || (data.detail ? { detail: [data.detail] } : data);
    } else if (typeof data === 'string' && data.length > 0) {
      message = data;
    }

    return {
      status,
      message,
      errors,
      raw: error.response,
    };
  }

  if (error.code === 'ECONNABORTED' || error.message?.toLowerCase().includes('timeout')) {
    return {
      status: 408,
      message: 'Request timed out. Please check your network connection and retry.',
      errors: { network: ['Connection timeout'] },
    };
  }

  if (error.request) {
    return {
      status: 0,
      message: 'Network error. Could not connect to the PawMatch server.',
      errors: { network: ['Server unreachable'] },
    };
  }

  return {
    status: 500,
    message: error.message || 'An unknown application error occurred.',
    errors: null,
  };
};

export default parseApiError;
