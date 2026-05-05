export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

export interface TokenData {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserData {
  username: string;
  role: string;
}

export interface MenuItem {
  key: string;
  title: string;
  icon?: string;
  path?: string;
  children?: MenuItem[];
  sort?: number;
}

export interface HealthData {
  status: string;
}
