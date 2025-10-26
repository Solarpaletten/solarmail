/**
 * API Client Tests
 * 
 * Run with: npm test
 */

import { APIClient } from "../lib/api";
import { APIError, NetworkError, TimeoutError, ValidationError } from "../lib/errors";

describe("APIClient", () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const api = new APIClient(apiUrl);

  describe("Health Check", () => {
    it("should successfully ping the API", async () => {
      const result = await api.ping();
      expect(result).toBe(true);
    });

    it("should return health status", async () => {
      const health = await api.healthCheck();
      expect(health).toHaveProperty("status");
      expect(health).toHaveProperty("version");
    });
  });

  describe("Email Operations", () => {
    it("should fetch emails with default limit", async () => {
      const emails = await api.getEmails();
      expect(Array.isArray(emails)).toBe(true);
      expect(emails.length).toBeLessThanOrEqual(20);
    });

    it("should fetch emails with custom limit", async () => {
      const limit = 5;
      const emails = await api.getEmails(limit);
      expect(emails.length).toBeLessThanOrEqual(limit);
    });

    it("should throw validation error for invalid limit", async () => {
      await expect(api.getEmails(0)).rejects.toThrow(ValidationError);
      await expect(api.getEmails(101)).rejects.toThrow(ValidationError);
    });

    it("should fetch single email by ID", async () => {
      const emails = await api.getEmails(1);
      if (emails.length > 0) {
        const email = await api.getEmail(emails[0].id);
        expect(email).toHaveProperty("id");
        expect(email).toHaveProperty("subject");
        expect(email).toHaveProperty("sender");
      }
    });

    it("should throw validation error for invalid email ID", async () => {
      await expect(api.getEmail(0)).rejects.toThrow(ValidationError);
      await expect(api.getEmail(-1)).rejects.toThrow(ValidationError);
    });
  });

  describe("Email Analysis", () => {
    it("should analyze email with subject and body", async () => {
      const analysis = await api.analyzeEmail(
        "Important Meeting Tomorrow",
        "Hi team, we have an urgent meeting scheduled for tomorrow at 10 AM."
      );

      expect(analysis).toHaveProperty("sentiment");
      expect(analysis).toHaveProperty("priority");
      expect(analysis).toHaveProperty("category");
      expect(analysis.sentiment_score).toBeGreaterThanOrEqual(0);
      expect(analysis.sentiment_score).toBeLessThanOrEqual(1);
    });

    it("should throw validation error for empty subject and body", async () => {
      await expect(api.analyzeEmail("", "")).rejects.toThrow(ValidationError);
    });

    it("should analyze with only subject", async () => {
      const analysis = await api.analyzeEmail("Test Subject", "");
      expect(analysis).toHaveProperty("sentiment");
    });

    it("should analyze with only body", async () => {
      const analysis = await api.analyzeEmail("", "Test body content");
      expect(analysis).toHaveProperty("sentiment");
    });
  });

  describe("Sync Operations", () => {
    it("should get sync status for valid email", async () => {
      const status = await api.getSyncStatus("test@example.com");
      expect(status).toHaveProperty("account_email");
      expect(status).toHaveProperty("last_sync_date");
    });

    it("should throw validation error for invalid email", async () => {
      await expect(api.getSyncStatus("invalid")).rejects.toThrow(ValidationError);
      await expect(api.getSyncStatus("")).rejects.toThrow(ValidationError);
    });

    it("should trigger sync", async () => {
      const result = await api.triggerSync();
      expect(result).toHaveProperty("status");
      expect(result).toHaveProperty("message");
    });
  });

  describe("Error Handling", () => {
    it("should handle 404 errors", async () => {
      try {
        await api.getEmail(999999);
        fail("Should have thrown an error");
      } catch (error) {
        expect(error).toBeInstanceOf(APIError);
        if (error instanceof APIError) {
          expect(error.statusCode).toBe(404);
        }
      }
    });

    it("should handle timeout", async () => {
      // This test requires a slow endpoint or mock
      // For now, just verify timeout error type exists
      expect(TimeoutError).toBeDefined();
    });

    it("should handle network errors", async () => {
      const invalidApi = new APIClient("http://invalid-url-that-does-not-exist");
      try {
        await invalidApi.ping();
      } catch (error) {
        expect(error).toBeInstanceOf(NetworkError);
      }
    });
  });

  describe("Utility Methods", () => {
    it("should return base URL", () => {
      const baseUrl = api.getBaseURL();
      expect(baseUrl).toContain("/api/v1");
    });
  });
});
