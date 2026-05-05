import { apiClient, setTokens, clearTokens } from "./client";
import type { ApiResponse } from "./client";

interface LoginRequest {
  username: string;
  password: string;
}

interface TokenData {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface UserData {
  username: string;
  role: string;
}

export async function login(data: LoginRequest): Promise<ApiResponse<TokenData>> {
  const resp = await apiClient.post<ApiResponse<TokenData>>(
    "/api/v1/admin/auth/login",
    data,
  );
  if (resp.code === 0) {
    setTokens(resp.data.access_token, resp.data.refresh_token);
  }
  return resp;
}

export async function logout(): Promise<ApiResponse<null>> {
  const resp = await apiClient.post<ApiResponse<null>>("/api/v1/admin/auth/logout");
  clearTokens();
  return resp;
}

export async function refreshToken(token: string): Promise<ApiResponse<TokenData>> {
  return apiClient.post<ApiResponse<TokenData>>(
    "/api/v1/admin/auth/refresh",
    { refresh_token: token },
  );
}

export async function getCurrentUser(): Promise<ApiResponse<UserData>> {
  return apiClient.get<ApiResponse<UserData>>("/api/v1/admin/auth/me");
}
