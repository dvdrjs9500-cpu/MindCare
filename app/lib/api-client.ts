/**
 * API Client Configuration for MindCare Frontend
 * Handles all communication with Django backend
 * Manages authentication tokens and API requests
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const API_ENDPOINTS = {
  // Auth
  AUTH_REGISTER: '/users/auth/register/',
  AUTH_LOGIN: '/users/auth/login/',
  AUTH_LOGOUT: '/users/auth/logout/',
  AUTH_PROFILE: '/users/auth/profile/',
  AUTH_UPDATE_PROFILE: '/users/auth/profile/update/',
  AUTH_USER_LIST: '/users/auth/users/',

  // Health Profile
  HEALTH_PROFILE: '/users/health-profile/',
  HEALTH_PROFILE_UPDATE: '/users/health-profile/update/',

  // Journal
  JOURNAL_ENTRIES: '/users/journal/',
  JOURNAL_ADD: '/users/journal/add/',
  JOURNAL_EDIT: (entryId) => `/users/journal/${entryId}/edit/`,
  JOURNAL_DELETE: (entryId) => `/users/journal/${entryId}/remove/`,

  // Quizzes
  QUIZ_LIST: '/assessments/quizzes/',
  QUIZ_TYPES: '/assessments/quizzes/types/',
  QUIZ_DETAIL: (quizId) => `/assessments/quizzes/${quizId}/`,
  QUIZ_SUBMIT: '/assessments/quiz-results/submit/',
  QUIZ_RESULTS: '/assessments/quiz-results/my-results/',

  // Videos
  VIDEO_UPLOAD: '/assessments/videos/upload/',
  VIDEO_ANALYSES: '/assessments/videos/my-analyses/',
  VIDEO_DETAIL: (analysisId) => `/assessments/videos/${analysisId}/`,

  // Assessment History
  ASSESSMENT_HISTORY: '/assessments/history/my-history/',
  ASSESSMENT_SUMMARY: '/assessments/history/summary/',

  // Clinics
  CLINIC_LIST: '/clinics/clinics/',
  CLINIC_DETAIL: (clinicId) => `/clinics/clinics/${clinicId}/`,
  CLINIC_CITIES: '/clinics/clinics/cities/',
  CLINIC_SPECIALIZATIONS: '/clinics/clinics/specializations/',
  CLINIC_NEAREST: '/clinics/recommendations/nearest/',
  CLINIC_RECOMMENDATIONS: '/clinics/recommendations/user/',
  CLINIC_MARK_CONTACTED: (recId) => `/clinics/recommendations/${recId}/mark-contacted/`,
  CLINIC_MARK_VIEWED: (recId) => `/clinics/recommendations/${recId}/mark-viewed/`,
};

/**
 * Token Management
 */
const TOKEN_KEY = 'mindcare_auth_token';
const USER_KEY = 'mindcare_user';

export const TokenManager = {
  getToken: () => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(TOKEN_KEY);
    }
    return null;
  },

  setToken: (token) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_KEY, token);
    }
  },

  removeToken: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }
  },

  getUser: () => {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem(USER_KEY);
      return userStr ? JSON.parse(userStr) : null;
    }
    return null;
  },

  setUser: (user) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    }
  },

  isAuthenticated: () => {
    return !!TokenManager.getToken();
  },
};

/**
 * API Error Handling
 */
export class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'APIError';
  }
}

/**
 * Fetch Wrapper with Authentication
 */
export const apiFetch = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = TokenManager.getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);

    // Handle response
    let data;
    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      throw new APIError(
        data?.detail || data?.error || 'API Error',
        response.status,
        data
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network Error', 0, error);
  }
};

/**
 * API Services
 */

// Authentication
export const AuthService = {
  register: async (username, email, password, password2, firstName, lastName) => {
    const response = await apiFetch(API_ENDPOINTS.AUTH_REGISTER, {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
        password,
        password2,
        first_name: firstName,
        last_name: lastName,
      }),
    });

    if (response.token) {
      TokenManager.setToken(response.token);
      TokenManager.setUser(response.user);
    }

    return response;
  },

  login: async (email, password) => {
    const response = await apiFetch(API_ENDPOINTS.AUTH_LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    if (response.token) {
      TokenManager.setToken(response.token);
      TokenManager.setUser(response.user);
    }

    return response;
  },

  logout: async () => {
    try {
      await apiFetch(API_ENDPOINTS.AUTH_LOGOUT, { method: 'POST' });
    } finally {
      TokenManager.removeToken();
    }
  },

  getProfile: () => apiFetch(API_ENDPOINTS.AUTH_PROFILE),

  updateProfile: (data) =>
    apiFetch(API_ENDPOINTS.AUTH_UPDATE_PROFILE, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
};

// Health Profile
export const HealthService = {
  getProfile: () => apiFetch(API_ENDPOINTS.HEALTH_PROFILE),

  updateProfile: (data) =>
    apiFetch(API_ENDPOINTS.HEALTH_PROFILE_UPDATE, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
};

// Journal
export const JournalService = {
  getEntries: (page = 1, pageSize = 10) =>
    apiFetch(`${API_ENDPOINTS.JOURNAL_ENTRIES}?page=${page}&page_size=${pageSize}`),

  addEntry: (data) =>
    apiFetch(API_ENDPOINTS.JOURNAL_ADD, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  editEntry: (entryId, data) =>
    apiFetch(API_ENDPOINTS.JOURNAL_EDIT(entryId), {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteEntry: (entryId) =>
    apiFetch(API_ENDPOINTS.JOURNAL_DELETE(entryId), {
      method: 'DELETE',
    }),
};

// Quizzes
export const QuizService = {
  listQuizzes: () => apiFetch(API_ENDPOINTS.QUIZ_LIST),

  getQuizTypes: () => apiFetch(API_ENDPOINTS.QUIZ_TYPES),

  getQuizDetail: (quizId) => apiFetch(API_ENDPOINTS.QUIZ_DETAIL(quizId)),

  submitQuiz: (data) =>
    apiFetch(API_ENDPOINTS.QUIZ_SUBMIT, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getResults: (page = 1, pageSize = 10) =>
    apiFetch(`${API_ENDPOINTS.QUIZ_RESULTS}?page=${page}&page_size=${pageSize}`),
};

// Videos
export const VideoService = {
  uploadVideo: (formData) =>
    apiFetch(API_ENDPOINTS.VIDEO_UPLOAD, {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it with boundary
    }),

  getAnalyses: (page = 1, pageSize = 10) =>
    apiFetch(`${API_ENDPOINTS.VIDEO_ANALYSES}?page=${page}&page_size=${pageSize}`),

  getAnalysisDetail: (analysisId) => apiFetch(API_ENDPOINTS.VIDEO_DETAIL(analysisId)),
};

// Assessment
export const AssessmentService = {
  getHistory: (page = 1, pageSize = 10, type = null) => {
    let url = `${API_ENDPOINTS.ASSESSMENT_HISTORY}?page=${page}&page_size=${pageSize}`;
    if (type) url += `&type=${type}`;
    return apiFetch(url);
  },

  getSummary: () => apiFetch(API_ENDPOINTS.ASSESSMENT_SUMMARY),
};

// Clinics
export const ClinicService = {
  listClinics: (city = null, specialization = null, minRating = null) => {
    let url = API_ENDPOINTS.CLINIC_LIST;
    const params = new URLSearchParams();
    if (city) params.append('city', city);
    if (specialization) params.append('specialization', specialization);
    if (minRating) params.append('min_rating', minRating);
    if (params.toString()) url += `?${params.toString()}`;
    return apiFetch(url);
  },

  getClinicDetail: (clinicId) => apiFetch(API_ENDPOINTS.CLINIC_DETAIL(clinicId)),

  getCities: () => apiFetch(API_ENDPOINTS.CLINIC_CITIES),

  getSpecializations: () => apiFetch(API_ENDPOINTS.CLINIC_SPECIALIZATIONS),

  getNearestClinics: (latitude, longitude, radius = 50, specialization = null) => {
    let url = `${API_ENDPOINTS.CLINIC_NEAREST}?latitude=${latitude}&longitude=${longitude}&radius=${radius}`;
    if (specialization) url += `&specialization=${specialization}`;
    return apiFetch(url);
  },

  getRecommendations: (page = 1, pageSize = 10) =>
    apiFetch(`${API_ENDPOINTS.CLINIC_RECOMMENDATIONS}?page=${page}&page_size=${pageSize}`),

  markContacted: (recId) =>
    apiFetch(API_ENDPOINTS.CLINIC_MARK_CONTACTED(recId), {
      method: 'PUT',
    }),

  markViewed: (recId) =>
    apiFetch(API_ENDPOINTS.CLINIC_MARK_VIEWED(recId), {
      method: 'PUT',
    }),
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  TokenManager,
  APIError,
  apiFetch,
  AuthService,
  HealthService,
  JournalService,
  QuizService,
  VideoService,
  AssessmentService,
  ClinicService,
};
