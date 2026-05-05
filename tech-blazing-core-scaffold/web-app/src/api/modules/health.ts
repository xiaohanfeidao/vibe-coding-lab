import { apiClient } from "../client";

interface HealthData {
  status: string;
}

export async function getHealth() {
  return apiClient.get<import("../client").ApiResponse<HealthData>>(
    "/api/v1/web/health",
  );
}
