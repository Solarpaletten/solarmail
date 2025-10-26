const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Email {
  id: number;
  uid: string;
  sender: string;
  subject: string;
  date: string;
  body_preview: string;
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
}

export interface SyncStatus {
  account_email: string;
  last_sync_date: string;
  last_sync_success: boolean;
  total_emails_synced: number;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.fetch("/health");
  }

  // Get emails
  async getEmails(limit: number = 20): Promise<Email[]> {
    return this.fetch(`/api/emails?limit=${limit}`);
  }

  // Get email by ID
  async getEmail(id: number): Promise<Email> {
    return this.fetch(`/api/emails/${id}`);
  }

  // Analyze email
  async analyzeEmail(subject: string, body: string): Promise<EmailAnalysis> {
    return this.fetch("/api/analyze", {
      method: "POST",
      body: JSON.stringify({ subject, body }),
    });
  }

  // Get sync status
  async getSyncStatus(email: string): Promise<SyncStatus> {
    return this.fetch(`/api/sync/status?email=${encodeURIComponent(email)}`);
  }

  // Trigger sync
  async triggerSync(): Promise<{ status: string; message: string }> {
    return this.fetch("/api/sync/trigger", {
      method: "POST",
    });
  }
}

export const api = new APIClient(API_BASE_URL);
