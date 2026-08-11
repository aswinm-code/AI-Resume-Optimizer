// src/api/auth.ts

import apiClient from "./client";

import type {
  AuthResponse,
  User,
} from "@/types";


// ============================================================
// LOGIN
// ============================================================

export interface LoginRequest {
  username: string;
  password: string;
}


/**
 * Login using FastAPI OAuth2 password authentication.
 *
 * FastAPI's OAuth2PasswordRequestForm expects:
 *
 * username
 * password
 *
 * as application/x-www-form-urlencoded data.
 */
export async function login(
  credentials: LoginRequest
): Promise<AuthResponse> {

  const formData = new URLSearchParams();

  formData.append(
    "username",
    credentials.username
  );

  formData.append(
    "password",
    credentials.password
  );

  const response = await apiClient.post<AuthResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
}


// ============================================================
// REGISTER
// ============================================================

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}


/**
 * Register a new user.
 *
 * IMPORTANT:
 * The exact request fields must match your FastAPI
 * registration schema.
 */
export async function register(
  data: RegisterRequest
): Promise<User> {

  const response = await apiClient.post<User>(
    "/auth/register",
    data
  );

  return response.data;
}


// ============================================================
// CURRENT USER
// ============================================================

/**
 * Get the currently authenticated user.
 *
 * The JWT is automatically added by apiClient.
 */
export async function getCurrentUser(): Promise<User> {

  const response = await apiClient.get<User>(
    "/users/me"
  );

  return response.data;
}


// ============================================================
// LOGOUT
// ============================================================

/**
 * JWT authentication is stateless on the backend.
 *
 * For now, logging out simply removes the token.
 */
export function logout(): void {

  localStorage.removeItem(
    "access_token"
  );
}