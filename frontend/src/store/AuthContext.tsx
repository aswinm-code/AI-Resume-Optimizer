// src/store/AuthContext.tsx

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  login as loginApi,
  register as registerApi,
  logout as logoutApi,
} from "@/api/authApi";

import type {
  LoginRequest,
  RegisterRequest,
} from "@/api/authApi";

import type {
  User,
} from "@/types";


// ============================================================
// CONTEXT TYPE
// ============================================================

interface AuthContextType {

  user: User | null;

  isAuthenticated: boolean;

  isLoading: boolean;

  login: (
    credentials: LoginRequest
  ) => Promise<void>;

  register: (
    data: RegisterRequest
  ) => Promise<void>;

  logout: () => void;
}


// ============================================================
// CONTEXT
// ============================================================

const AuthContext =
  createContext<AuthContextType | undefined>(
    undefined
  );


// ============================================================
// PROVIDER
// ============================================================

interface AuthProviderProps {
  children: ReactNode;
}


export function AuthProvider({
  children,
}: AuthProviderProps) {

  const [user, setUser] =
    useState<User | null>(null);

  const [isLoading, setIsLoading] =
    useState(true);


  // ----------------------------------------------------------
  // Restore authentication when application starts
  // ----------------------------------------------------------

  useEffect(() => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    if (!token) {

      setIsLoading(false);

      return;
    }


    getCurrentUser()

      .then((currentUser) => {

        setUser(currentUser);

      })

      .catch(() => {

        localStorage.removeItem(
          "access_token"
        );

        setUser(null);

      })

      .finally(() => {

        setIsLoading(false);

      });

  }, []);


  // ----------------------------------------------------------
  // LOGIN
  // ----------------------------------------------------------

  const login = async (
    credentials: LoginRequest
  ): Promise<void> => {

    const response =
      await loginApi(credentials);


    localStorage.setItem(
      "access_token",
      response.access_token
    );


    /*
     * Login response may or may not contain
     * the user object.
     *
     * Therefore fetch the authenticated user
     * from /users/me.
     */

    const currentUser =
      await getCurrentUser();


    setUser(currentUser);
  };


  // ----------------------------------------------------------
  // REGISTER
  // ----------------------------------------------------------

  const register = async (
    data: RegisterRequest
  ): Promise<void> => {

    await registerApi(data);

    /*
     * We deliberately don't automatically
     * assume registration logs the user in.
     *
     * Login is performed explicitly after
     * successful registration.
     */
  };


  // ----------------------------------------------------------
  // LOGOUT
  // ----------------------------------------------------------

  const logout = (): void => {

    logoutApi();

    setUser(null);
  };


  // ----------------------------------------------------------
  // CONTEXT VALUE
  // ----------------------------------------------------------

  const value: AuthContextType = {

    user,

    isAuthenticated:
      user !== null,

    isLoading,

    login,

    register,

    logout,
  };


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}


// ============================================================
// HOOK
// ============================================================

export function useAuth(): AuthContextType {

  const context =
    useContext(AuthContext);


  if (!context) {

    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }


  return context;
}