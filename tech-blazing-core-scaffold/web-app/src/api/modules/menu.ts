import { apiClient } from "../client";

interface MenuItem {
  key: string;
  title: string;
  icon?: string;
  path?: string;
  children?: MenuItem[];
  sort?: number;
}

export async function getMenus() {
  return apiClient.get<import("../client").ApiResponse<MenuItem[]>>(
    "/api/v1/web/menus",
  );
}

export type { MenuItem };
