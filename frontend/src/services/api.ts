import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface QueryRequest {
  question: string;
  db_hint?: string;
  max_tables?: number;
}

export interface SQLResponse {
  db: string;
  answer: string;
  sql_query: string;
  intermediate_steps: unknown[];
}

export interface TableSearchResponse {
  query: string;
  relevant_tables: string[];
  metadata: Record<string, unknown>;
  count: number;
}

export interface HealthResponse {
  status: string;
  databases: string[];
  total_tables: number;
  available_tables: string[];
}

export const sqlAPI = {
  // Execute SQL query
  executeQuery: async (request: QueryRequest): Promise<SQLResponse> => {
    const response = await api.post<SQLResponse>("/ask-sql", request);
    return response.data;
  },

  // Get health status
  getHealth: async (): Promise<HealthResponse> => {
    const response = await api.get<HealthResponse>("/health");
    return response.data;
  },

  // Search tables
  searchTables: async (
    query: string,
    maxResults: number = 5
  ): Promise<TableSearchResponse> => {
    const response = await api.get<TableSearchResponse>("/tables/search", {
      params: { query, max_results: maxResults },
    });
    return response.data;
  },

  // Get all tables
  getTables: async (): Promise<{ tables: string[]; count: number }> => {
    const response = await api.get("/tables");
    return response.data;
  },
};

export default api;
