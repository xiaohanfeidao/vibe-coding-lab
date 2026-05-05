import { apiClient } from "../client";
import type { ApiResponse } from "../client";

interface MenuItem {
  key: string;
  title: string;
  icon?: string;
  path?: string;
  children?: MenuItem[];
  sort?: number;
}

export async function getAdminMenus() {
  return apiClient.get<ApiResponse<MenuItem[]>>("/api/v1/admin/menus");
}

export type { MenuItem };
