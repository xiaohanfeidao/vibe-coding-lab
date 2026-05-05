export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

export interface HealthData {
  status: string;
}

export interface MenuItem {
  key: string;
  title: string;
  icon?: string;
  path?: string;
  children?: MenuItem[];
  sort?: number;
}
