import axios from "axios";
import type { AxiosInstance, AxiosResponse } from "axios";
import { Message } from "@arco-design/web-react";

interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

function createApiClient(baseURL: string): AxiosInstance {
  const client = axios.create({ baseURL, timeout: 10000 });

  client.interceptors.response.use(
    (response: AxiosResponse<ApiResponse>) => response.data,
    (error) => {
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
