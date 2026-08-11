// src/api/client.ts

import axios, {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";


// ============================================================
// API CONFIGURATION
// ============================================================

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "/api";


// ============================================================
// AXIOS CLIENT
// ============================================================

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,

  headers: {
    Accept: "application/json",
  },

  timeout: 120000,
});


// ============================================================
// REQUEST INTERCEPTOR
// Adds JWT token to every authenticated request
// ============================================================

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {

    const token = localStorage.getItem("access_token");

    if (token) {

      config.headers.Authorization = `Bearer ${token}`;

    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);


// ============================================================
// RESPONSE INTERCEPTOR
// Handles authentication failures centrally
// ============================================================

apiClient.interceptors.response.use(

  (response) => {
    return response;
  },

  (error: AxiosError) => {

    if (error.response?.status === 401) {

      /*
       * Do not automatically redirect here.
       *
       * AuthContext / protected routes will handle
       * authentication state.
       */

      localStorage.removeItem("access_token");
    }

    return Promise.reject(error);
  }
);


// ============================================================
// ERROR HELPER
// Converts FastAPI errors into a usable message
// ============================================================

export function getApiErrorMessage(
  error: unknown
): string {

  if (axios.isAxiosError(error)) {

    const detail = error.response?.data?.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {

      return detail
        .map((item) => {

          if (
            typeof item === "object" &&
            item !== null &&
            "msg" in item
          ) {
            return String(item.msg);
          }

          return String(item);
        })
        .join(", ");
    }

    if (
      error.response?.data?.message &&
      typeof error.response.data.message === "string"
    ) {
      return error.response.data.message;
    }

    if (error.message) {
      return error.message;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong. Please try again.";
}

export function readError(error: unknown, fallback = "Something went wrong. Please try again.") {
  const message = getApiErrorMessage(error);
  return message || fallback;
}

// ============================================================
// EXPORT
// ============================================================

export default apiClient;