import { useState, useEffect } from "react";
import type { ApiResponse } from "../api/client";

export function useRequest<T>(
  requestFn: () => Promise<ApiResponse<T>>,
  immediate = true,
) {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(immediate);
  const [error, setError] = useState<Error | null>(null);

  const execute = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await requestFn();
      setData(response.data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, []);

  return { data, isLoading, error, refetch: execute };
}
