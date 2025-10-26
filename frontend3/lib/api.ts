import { APIError, NetworkError, TimeoutError, ValidationError } from "./errors";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_VERSION = "/api/v1";
const DEFAULT_TIMEOUT = 10000; // 10 seconds

export interface Email {
  id: number;
  uid: string;
  sender: string;
  subject: string;
  date: string;
  body_preview: string;
  body?: string;
}

export interface EmailAnalysis {
  sentiment: string;
  sentiment_score: number;
  priority: string;
  priority_score: number;
  category: string;
  category_confidence: number;
  entities_json: string;
  keywords_json: string;
  ai_model?: string;
  processing_time_ms?: number;
}

export interface SyncStatus {
  account_email: string;
  last_sync_date: string;
  last_sync_success: boolean;
  total_emails_synced: number;
  last_error_message?: string;
}

export interface HealthStatus {
  status: string;
  version: string;
  timestamp?: string;
}

export interface AnalyzeRequest {
  subject: string;
  body: string;
}

/**
 * Fetch with timeout support
 */
async function fetchWithTimeout(
  url: string,
  options?: RequestInit,
  timeout: number = DEFAULT_TIMEOUT
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === "AbortError") {
      throw new TimeoutError(`Request timeout after ${timeout}ms`);
    }
    throw error;
  }
}

/**
 * API Client for SolarMail Backend
 */
class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL + API_VERSION;
  }

  /**
   * Generic fetch method with error handling
   */
  private async fetch<T>(
    endpoint: string,
    options?: RequestInit,
    timeout?: number
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetchWithTimeout(
        url,
        {
          ...options,
          headers: {
            "Content-Type": "application/json",
            ...options?.headers,
          },
        },
        timeout
      );

      // Handle HTTP errors
      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch {
          // If response is not JSON, use status text
        }

        throw new APIError(errorMessage, response.status, endpoint);
      }

      // Parse JSON response
      const data = await response.json();
      return data;
    } catch (error) {
      // Re-throw custom errors
      if (
        error instanceof APIError ||
        error instanceof TimeoutError ||
        error instanceof ValidationError
      ) {
        throw error;
      }

      // Handle network errors
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new NetworkError("Failed to connect to API server");
      }

      // Unknown error
      throw new APIError(
        error instanceof Error ? error.message : "Unknown error occurred",
        undefined,
        endpoint
      );
    }
  }

  /**
   * Health check - verify API is running
   */
  async healthCheck(): Promise<HealthStatus> {
    return this.fetch<HealthStatus>("/health");
  }

  /**
   * Get list of emails
   */
  async getEmails(limit: number = 20): Promise<Email[]> {
    if (limit < 1 || limit > 100) {
      throw new ValidationError("Limit must be between 1 and 100");
    }
    return this.fetch<Email[]>(`/emails?limit=${limit}`);
  }

  /**
   * Get single email by ID
   */
  async getEmail(id: number): Promise<Email> {
    if (!id || id < 1) {
      throw new ValidationError("Invalid email ID");
    }
    return this.fetch<Email>(`/emails/${id}`);
  }

  /**
   * Analyze email content
   */
  async analyzeEmail(subject: string, body: string): Promise<EmailAnalysis> {
    if (!subject && !body) {
      throw new ValidationError("Subject or body is required");
    }

    const request: AnalyzeRequest = { subject, body };
    return this.fetch<EmailAnalysis>("/analyze", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  /**
   * Get sync status for an email account
   */
  async getSyncStatus(email: string): Promise<SyncStatus> {
    if (!email || !email.includes("@")) {
      throw new ValidationError("Invalid email address");
    }
    return this.fetch<SyncStatus>(`/sync/status?email=${encodeURIComponent(email)}`);
  }

  /**
   * Trigger email synchronization
   */
  async triggerSync(): Promise<{ status: string; message: string }> {
    return this.fetch<{ status: string; message: string }>("/sync/trigger", {
      method: "POST",
    });
  }

  /**
   * Check if API is reachable (lightweight health check)
   */
  async ping(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get API base URL (for debugging)
   */
  getBaseURL(): string {
    return this.baseURL;
  }
}

// Export singleton instance
export const api = new APIClient(API_BASE_URL);

// Export class for testing
export { APIClient };
