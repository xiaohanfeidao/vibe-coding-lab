import { apiClient } from "../client";
import type { ApiResponse } from "../client";

interface HealthData {
  status: string;
}

export async function getHealth() {
  return apiClient.get<ApiResponse<HealthData>>("/api/v1/admin/health");
}
