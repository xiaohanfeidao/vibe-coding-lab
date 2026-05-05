import axios from "axios";
import type { AxiosInstance, AxiosResponse } from "axios";
import { Message } from "@arco-design/web-react";

interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
}

export function getAccessToken(): string | null {
  return accessToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}

function createApiClient(baseURL: string): AxiosInstance {
  const client = axios.create({ baseURL, timeout: 10000 });

  client.interceptors.request.use((config) => {
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  });

  client.interceptors.response.use(
    (response: AxiosResponse<ApiResponse>) => response.data,
    async (error) => {
      const originalRequest = error.config;

      if (error.response?.status === 401 && !originalRequest._retry && refreshToken) {
        originalRequest._retry = true;
        try {
          const resp = await axios.post(
            `${baseURL}/api/v1/admin/auth/refresh`,
            { refresh_token: refreshToken },
          );
          const data = resp.data.data;
          setTokens(data.access_token, data.refresh_token);
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
          return client(originalRequest);
        } catch {
          clearTokens();
          window.location.href = "/login";
          return Promise.reject(error);
        }
      }

      const msg = error.response?.data?.message ?? "请求失败";
      Message.error(msg);
      return Promise.reject(error);
    },
  );

  return client;
}

export const apiClient = createApiClient(
  import.meta.env.VITE_API_BASE_URL ?? "",
);

export type { ApiResponse };
