const API_BASE_URL = 'http://localhost:8000/api'; // Adjust if needed

export const api = {
  register: async (userData) => {
    const endpoint = userData.role === 'provider' ? 'register/provider/' : 'register/';
    const response = await fetch(`${API_BASE_URL}/users/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    if (!response.ok) {
      throw new Error('Registration failed');
    }
    return response.json();
  },

  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/users/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    if (!response.ok) {
      throw new Error('Login failed');
    }
    const data = await response.json();
    // Store tokens
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  },

  // Add more API functions as needed
};