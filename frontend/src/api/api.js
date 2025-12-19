import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Base URL - update this based on your environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          // Try to refresh the token
          const response = await axios.post(
            `${API_BASE_URL}/auth/refresh/`,
            { refresh: refreshToken }
          );
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed - logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Helper function to check if token is expired
const isTokenExpired = (token) => {
  if (!token) return true;
  try {
    const decoded = jwtDecode(token);
    return decoded.exp * 1000 < Date.now();
  } catch (error) {
    return true;
  }
};

// Helper function to get current user from token
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (error) {
      localStorage.removeItem('user');
      return null;
    }
  }
  return null;
};

// Helper function to check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem('access_token');
  return token && !isTokenExpired(token);
};

// Helper function to get user role
export const getUserRole = () => {
  const user = getCurrentUser();
  return user?.role || null;
};

// Authentication API calls
export const authAPI = {
  // Register new user
  register: async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  // Login
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  // Logout
  logout: async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  // Get user profile
  getProfile: async () => {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  // Update user profile
  updateProfile: async (profileData) => {
    const response = await api.put('/auth/profile/update/', profileData);
    if (response.data) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  },

  // Refresh token
  refreshToken: async (refreshToken) => {
    const response = await api.post('/auth/refresh/', { refresh: refreshToken });
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
    }
    return response.data;
  },
};

// Users API calls (Admin only)
export const usersAPI = {
  // Get all users (admin only)
  getAllUsers: async (params = {}) => {
    const response = await api.get('/users/', { params });
    return response.data;
  },

  // Get user by ID (admin only)
  getUserById: async (userId) => {
    const response = await api.get(`/users/${userId}/`);
    return response.data;
  },

  // Update user (admin only)
  updateUser: async (userId, userData) => {
    const response = await api.put(`/users/${userId}/`, userData);
    return response.data;
  },

  // Delete user (admin only)
  deleteUser: async (userId) => {
    const response = await api.delete(`/users/${userId}/`);
    return response.data;
  },
};

// Services API calls
export const servicesAPI = {
  // Get all services
  getAllServices: async (params = {}) => {
    const response = await api.get('/services/', { params });
    return response.data;
  },

  // Get service by ID
  getServiceById: async (serviceId) => {
    const response = await api.get(`/services/${serviceId}/`);
    return response.data;
  },

  // Create service (provider only)
  createService: async (serviceData) => {
    const response = await api.post('/services/create/', serviceData);
    return response.data;
  },

  // Update service (provider only)
  updateService: async (serviceId, serviceData) => {
    const response = await api.put(`/services/${serviceId}/update/`, serviceData);
    return response.data;
  },

  // Get service categories
  getCategories: async () => {
    const response = await api.get('/services/categories/');
    return response.data;
  },

  // Get service packages
  getPackages: async (serviceId = null) => {
    const params = serviceId ? { service_id: serviceId } : {};
    const response = await api.get('/services/packages/', { params });
    return response.data;
  },

  // Get service requests
  getServiceRequests: async (params = {}) => {
    const response = await api.get('/services/requests/', { params });
    return response.data;
  },

  // Create service request (customer only)
  createServiceRequest: async (requestData) => {
    const response = await api.post('/services/requests/', requestData);
    return response.data;
  },

  // Get service request by ID
  getServiceRequestById: async (requestId) => {
    const response = await api.get(`/services/requests/${requestId}/`);
    return response.data;
  },

  // Update service request
  updateServiceRequest: async (requestId, requestData) => {
    const response = await api.put(`/services/requests/${requestId}/`, requestData);
    return response.data;
  },

  // Delete service request
  deleteServiceRequest: async (requestId) => {
    const response = await api.delete(`/services/requests/${requestId}/`);
    return response.data;
  },
};

// Providers API calls
export const providersAPI = {
  // Get all providers
  getAllProviders: async (params = {}) => {
    const response = await api.get('/providers/', { params });
    return response.data;
  },

  // Get provider by ID
  getProviderById: async (providerId) => {
    const response = await api.get(`/providers/${providerId}/`);
    return response.data;
  },

  // Get top providers
  getTopProviders: async () => {
    const response = await api.get('/providers/top/');
    return response.data;
  },

  // Register as provider
  registerProvider: async (providerData) => {
    const response = await api.post('/providers/register/', providerData);
    return response.data;
  },

  // Get provider profile (authenticated provider only)
  getProviderProfile: async () => {
    const response = await api.get('/providers/profile/');
    return response.data;
  },

  // Update provider profile
  updateProviderProfile: async (profileData) => {
    const response = await api.put('/providers/profile/update/', profileData);
    return response.data;
  },

  // Get provider's services
  getProviderServices: async () => {
    const response = await api.get('/providers/profile/services/');
    return response.data;
  },

  // Get provider documents
  getProviderDocuments: async () => {
    const response = await api.get('/providers/profile/documents/');
    return response.data;
  },

  // Upload provider document
  uploadDocument: async (documentData) => {
    const formData = new FormData();
    Object.keys(documentData).forEach(key => {
      formData.append(key, documentData[key]);
    });
    
    const response = await api.post('/providers/profile/documents/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Get provider availability
  getProviderAvailability: async () => {
    const response = await api.get('/providers/profile/availability/');
    return response.data;
  },

  // Set provider availability
  setAvailability: async (availabilityData) => {
    const response = await api.post('/providers/profile/availability/', availabilityData);
    return response.data;
  },

  // Get provider statistics
  getProviderStats: async () => {
    const response = await api.get('/providers/profile/stats/');
    return response.data;
  },
};

// Bookings API calls
export const bookingsAPI = {
  // Get all bookings (user-specific)
  getAllBookings: async (params = {}) => {
    const response = await api.get('/bookings/', { params });
    return response.data;
  },

  // Get booking by ID
  getBookingById: async (bookingId) => {
    const response = await api.get(`/bookings/${bookingId}/`);
    return response.data;
  },

  // Create booking (customer only)
  createBooking: async (bookingData) => {
    const response = await api.post('/bookings/', bookingData);
    return response.data;
  },

  // Update booking
  updateBooking: async (bookingId, bookingData) => {
    const response = await api.put(`/bookings/${bookingId}/`, bookingData);
    return response.data;
  },

  // Delete booking
  deleteBooking: async (bookingId) => {
    const response = await api.delete(`/bookings/${bookingId}/`);
    return response.data;
  },

  // Update booking status (provider only)
  updateBookingStatus: async (bookingId, statusData) => {
    const response = await api.post(`/bookings/${bookingId}/status/`, statusData);
    return response.data;
  },

  // Get customer bookings
  getCustomerBookings: async () => {
    const response = await api.get('/bookings/customer/bookings/');
    return response.data;
  },

  // Get provider bookings
  getProviderBookings: async () => {
    const response = await api.get('/bookings/provider/bookings/');
    return response.data;
  },

  // Get upcoming bookings
  getUpcomingBookings: async () => {
    const response = await api.get('/bookings/upcoming/');
    return response.data;
  },

  // Get booking statistics
  getBookingStats: async () => {
    const response = await api.get('/bookings/stats/');
    return response.data;
  },

  // Get booking attachments
  getBookingAttachments: async (bookingId) => {
    const response = await api.get(`/bookings/${bookingId}/attachments/`);
    return response.data;
  },

  // Upload booking attachment
  uploadAttachment: async (bookingId, attachmentData) => {
    const formData = new FormData();
    Object.keys(attachmentData).forEach(key => {
      formData.append(key, attachmentData[key]);
    });
    
    const response = await api.post(`/bookings/${bookingId}/attachments/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

// Payments API calls
export const paymentsAPI = {
  // Get all payments (user-specific)
  getAllPayments: async (params = {}) => {
    const response = await api.get('/payments/', { params });
    return response.data;
  },

  // Get payment by ID
  getPaymentById: async (paymentId) => {
    const response = await api.get(`/payments/${paymentId}/`);
    return response.data;
  },

  // Create payment
  createPayment: async (paymentData) => {
    const response = await api.post('/payments/', paymentData);
    return response.data;
  },

  // Create refund (admin only)
  createRefund: async (refundData) => {
    const response = await api.post('/payments/refunds/', refundData);
    return response.data;
  },

  // Get refund by ID (admin only)
  getRefundById: async (refundId) => {
    const response = await api.get(`/payments/refunds/${refundId}/`);
    return response.data;
  },

  // Get wallet details
  getWallet: async () => {
    const response = await api.get('/payments/wallet/');
    return response.data;
  },

  // Get wallet transactions
  getWalletTransactions: async () => {
    const response = await api.get('/payments/wallet/transactions/');
    return response.data;
  },

  // Deposit to wallet
  depositToWallet: async (depositData) => {
    const response = await api.post('/payments/wallet/deposit/', depositData);
    return response.data;
  },

  // Withdraw from wallet
  withdrawFromWallet: async (withdrawData) => {
    const response = await api.post('/payments/wallet/withdraw/', withdrawData);
    return response.data;
  },

  // Get payment statistics (admin only)
  getPaymentStats: async () => {
    const response = await api.get('/payments/stats/');
    return response.data;
  },
};

// Reviews API calls
export const reviewsAPI = {
  // Get all reviews
  getAllReviews: async (params = {}) => {
    const response = await api.get('/reviews/', { params });
    return response.data;
  },

  // Get review by ID
  getReviewById: async (reviewId) => {
    const response = await api.get(`/reviews/${reviewId}/`);
    return response.data;
  },

  // Create review (customer only)
  createReview: async (reviewData) => {
    const response = await api.post('/reviews/create/', reviewData);
    return response.data;
  },

  // Update review
  updateReview: async (reviewId, reviewData) => {
    const response = await api.put(`/reviews/${reviewId}/`, reviewData);
    return response.data;
  },

  // Delete review
  deleteReview: async (reviewId) => {
    const response = await api.delete(`/reviews/${reviewId}/`);
    return response.data;
  },

  // Mark review as helpful
  markHelpful: async (reviewId) => {
    const response = await api.post(`/reviews/${reviewId}/helpful/`);
    return response.data;
  },

  // Get provider reviews
  getProviderReviews: async (providerId) => {
    const response = await api.get(`/reviews/providers/${providerId}/reviews/`);
    return response.data;
  },

  // Get top rated providers
  getTopRatedProviders: async () => {
    const response = await api.get('/reviews/providers/top-rated/');
    return response.data;
  },

  // Upload review images
  uploadReviewImages: async (reviewId, imageData) => {
    const formData = new FormData();
    Object.keys(imageData).forEach(key => {
      formData.append(key, imageData[key]);
    });
    
    const response = await api.post(`/reviews/${reviewId}/images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Create provider report (customer only)
  createProviderReport: async (reportData) => {
    const response = await api.post('/reviews/reports/', reportData);
    return response.data;
  },

  // Get provider reports (admin only)
  getProviderReports: async () => {
    const response = await api.get('/reviews/reports/list/');
    return response.data;
  },

  // Get provider report by ID (admin only)
  getProviderReportById: async (reportId) => {
    const response = await api.get(`/reviews/reports/${reportId}/`);
    return response.data;
  },
};

// Notifications API calls
export const notificationsAPI = {
  // Get all notifications
  getAllNotifications: async (params = {}) => {
    const response = await api.get('/notifications/', { params });
    return response.data;
  },

  // Get notification by ID
  getNotificationById: async (notificationId) => {
    const response = await api.get(`/notifications/${notificationId}/`);
    return response.data;
  },

  // Delete notification
  deleteNotification: async (notificationId) => {
    const response = await api.delete(`/notifications/${notificationId}/`);
    return response.data;
  },

  // Mark notifications as read
  markAsRead: async (notificationIds) => {
    const response = await api.post('/notifications/mark-read/', { notification_ids: notificationIds });
    return response.data;
  },

  // Mark all notifications as read
  markAllAsRead: async () => {
    const response = await api.post('/notifications/mark-all-read/');
    return response.data;
  },

  // Get notification count
  getNotificationCount: async () => {
    const response = await api.get('/notifications/count/');
    return response.data;
  },

  // Get notification preferences
  getNotificationPreferences: async () => {
    const response = await api.get('/notifications/preferences/');
    return response.data;
  },

  // Update notification preferences
  updateNotificationPreferences: async (preferencesData) => {
    const response = await api.put('/notifications/preferences/', preferencesData);
    return response.data;
  },
};

// Export the main api instance and helper functions
export {
  api as default,
  API_BASE_URL,
  isAuthenticated,
  getCurrentUser,
  getUserRole,
};