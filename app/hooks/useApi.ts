/**
 * Custom React Hooks for MindCare API
 * Provides easy-to-use hooks for API operations with loading/error states
 */

import { useState, useCallback, useEffect } from 'react';
import {
  AuthService,
  HealthService,
  JournalService,
  QuizService,
  VideoService,
  AssessmentService,
  ClinicService,
  TokenManager,
  APIError,
} from './api-client';

/**
 * Generic async hook factory
 */
const useAsync = (asyncFunction, immediate = true) => {
  const [status, setStatus] = useState('idle');
  const [value, setValue] = useState(null);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...params) => {
      setStatus('pending');
      setValue(null);
      setError(null);

      try {
        const response = await asyncFunction(...params);
        setValue(response);
        setStatus('success');
        return response;
      } catch (err) {
        setError(err);
        setStatus('error');
        throw err;
      }
    },
    [asyncFunction]
  );

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { execute, status, value, error };
};

/**
 * Authentication Hooks
 */
export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const user = TokenManager.getUser();
    setUser(user);
    setIsAuthenticated(TokenManager.isAuthenticated());
  }, []);

  const register = useCallback(async (username, email, password, password2, firstName, lastName) => {
    setLoading(true);
    setError(null);
    try {
      const response = await AuthService.register(username, email, password, password2, firstName, lastName);
      setUser(response.user);
      setIsAuthenticated(true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await AuthService.login(email, password);
      setUser(response.user);
      setIsAuthenticated(true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await AuthService.logout();
      setUser(null);
      setIsAuthenticated(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const getProfile = useCallback(async () => {
    setLoading(true);
    try {
      const profile = await AuthService.getProfile();
      setUser(profile);
      return profile;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    user,
    isAuthenticated,
    loading,
    error,
    register,
    login,
    logout,
    getProfile,
  };
};

/**
 * Quiz Hooks
 */
export const useQuiz = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [quizDetail, setQuizDetail] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const listQuizzes = useCallback(async () => {
    setLoading(true);
    try {
      const data = await QuizService.listQuizzes();
      setQuizzes(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getQuizDetail = useCallback(async (quizId) => {
    setLoading(true);
    try {
      const data = await QuizService.getQuizDetail(quizId);
      setQuizDetail(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const submitQuiz = useCallback(async (quizData) => {
    setLoading(true);
    try {
      const result = await QuizService.submitQuiz(quizData);
      setResults([result, ...results]);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [results]);

  const getResults = useCallback(async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const data = await QuizService.getResults(page, pageSize);
      setResults(data.results || data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    quizzes,
    quizDetail,
    results,
    loading,
    error,
    listQuizzes,
    getQuizDetail,
    submitQuiz,
    getResults,
  };
};

/**
 * Video Hooks
 */
export const useVideo = () => {
  const [analyses, setAnalyses] = useState([]);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const uploadVideo = useCallback(async (videoFile) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('video', videoFile);

      const result = await VideoService.uploadVideo(formData);
      setAnalyses([result, ...analyses]);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [analyses]);

  const getAnalyses = useCallback(async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const data = await VideoService.getAnalyses(page, pageSize);
      setAnalyses(data.results || data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getAnalysisDetail = useCallback(async (analysisId) => {
    setLoading(true);
    try {
      const data = await VideoService.getAnalysisDetail(analysisId);
      setCurrentAnalysis(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    analyses,
    currentAnalysis,
    loading,
    error,
    uploadVideo,
    getAnalyses,
    getAnalysisDetail,
  };
};

/**
 * Assessment History Hook
 */
export const useAssessment = () => {
  const [history, setHistory] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getHistory = useCallback(async (page = 1, pageSize = 10, type = null) => {
    setLoading(true);
    try {
      const data = await AssessmentService.getHistory(page, pageSize, type);
      setHistory(data.results || data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getSummary = useCallback(async () => {
    setLoading(true);
    try {
      const data = await AssessmentService.getSummary();
      setSummary(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    history,
    summary,
    loading,
    error,
    getHistory,
    getSummary,
  };
};

/**
 * Clinic Hooks
 */
export const useClinic = () => {
  const [clinics, setClinics] = useState([]);
  const [cities, setCities] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [nearestClinics, setNearestClinics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const listClinics = useCallback(async (city = null, specialization = null, minRating = null) => {
    setLoading(true);
    try {
      const data = await ClinicService.listClinics(city, specialization, minRating);
      setClinics(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getCities = useCallback(async () => {
    setLoading(true);
    try {
      const data = await ClinicService.getCities();
      setCities(data.cities || []);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getSpecializations = useCallback(async () => {
    setLoading(true);
    try {
      const data = await ClinicService.getSpecializations();
      setSpecializations(data.specializations || []);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getNearestClinics = useCallback(async (latitude, longitude, radius = 50, specialization = null) => {
    setLoading(true);
    try {
      const data = await ClinicService.getNearestClinics(latitude, longitude, radius, specialization);
      setNearestClinics(Array.isArray(data) ? data : data.results || []);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    clinics,
    cities,
    specializations,
    nearestClinics,
    loading,
    error,
    listClinics,
    getCities,
    getSpecializations,
    getNearestClinics,
  };
};

export default {
  useAuth,
  useQuiz,
  useVideo,
  useAssessment,
  useClinic,
};
