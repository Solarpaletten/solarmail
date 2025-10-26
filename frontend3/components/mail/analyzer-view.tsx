"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, Users, FileText } from "lucide-react";
import { api, Email, EmailAnalysis } from "@/lib/api";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { InlineError } from "@/components/ui/error-display";

const sentimentColors = {
  positive: "success",
  neutral: "secondary",
  negative: "destructive",
} as const;

interface ParsedEntities {
  persons?: string[];
  organizations?: string[];
  topics?: string[];
}

interface ParsedKeywords {
  keywords?: string[];
}

export function AnalyzerView() {
  const [email, setEmail] = useState<Email | null>(null);
  const [analysis, setAnalysis] = useState<EmailAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);

    try {
      // Get first email
      const emails = await api.getEmails(1);
      if (emails.length === 0) {
        setError("No emails available for analysis");
        setLoading(false);
        return;
      }

      const firstEmail = emails[0];
      setEmail(firstEmail);

      // Analyze the email
      const analysisData = await api.analyzeEmail(
        firstEmail.subject,
        firstEmail.body_preview || ""
      );
      setAnalysis(analysisData);
    } catch (err) {
      console.error("Failed to analyze email:", err);
      setError(
        err instanceof Error ? err.message : "Failed to analyze email. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <LoadingSpinner size="lg" label="Analyzing email..." />
      </div>
    );
  }

  if (error) {
    return <InlineError message={error} onRetry={fetchAnalysis} />;
  }

  if (!analysis || !email) {
    return (
      <Card>
        <CardContent className="flex h-64 items-center justify-center">
          <div className="text-center text-muted-foreground">
            <Brain className="mx-auto mb-2 h-12 w-12 opacity-50" />
            <p>No analysis available</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Parse JSON fields
  let entities: ParsedEntities = {};
  let keywords: ParsedKeywords = {};

  try {
    entities = JSON.parse(analysis.entities_json || "{}");
  } catch {
    console.warn("Failed to parse entities_json");
  }

  try {
    keywords = JSON.parse(analysis.keywords_json || "{}");
  } catch {
    console.warn("Failed to parse keywords_json");
  }

  return (
    <div className="space-y-4">
      {/* Email Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Analyzing Email</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground">From: {email.sender}</p>
          <p className="text-sm font-medium">{email.subject}</p>
        </CardContent>
      </Card>

      {/* AI Analysis Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Brain className="h-5 w-5 text-primary" />
            AI Analysis
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Sentiment */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Sentiment</span>
              <Badge
                variant={
                  sentimentColors[analysis.sentiment as keyof typeof sentimentColors] ||
                  "secondary"
                }
              >
                {analysis.sentiment}
              </Badge>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
              <div
                className="h-full bg-green-500 transition-all"
                style={{ width: `${analysis.sentiment_score * 100}%` }}
              />
            </div>
            <span className="text-xs text-muted-foreground">
              Score: {(analysis.sentiment_score * 100).toFixed(0)}%
            </span>
          </div>

          {/* Priority */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Priority</span>
              <Badge
                variant={
                  analysis.priority === "high"
                    ? "destructive"
                    : analysis.priority === "medium"
                      ? "warning"
                      : "secondary"
                }
              >
                {analysis.priority}
              </Badge>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
              <div
                className="h-full bg-red-500 transition-all"
                style={{ width: `${analysis.priority_score * 100}%` }}
              />
            </div>
            <span className="text-xs text-muted-foreground">
              Score: {(analysis.priority_score * 100).toFixed(0)}%
            </span>
          </div>

          {/* Category */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Category</span>
              <Badge variant="outline">{analysis.category}</Badge>
            </div>
            <span className="text-xs text-muted-foreground">
              Confidence: {(analysis.category_confidence * 100).toFixed(0)}%
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Entities Card */}
      {(entities.persons?.length ||
        entities.organizations?.length ||
        entities.topics?.length) && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Users className="h-5 w-5 text-primary" />
              Detected Entities
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {entities.persons && entities.persons.length > 0 && (
              <div>
                <span className="text-xs font-medium text-muted-foreground">Persons</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {entities.persons.map((person, idx) => (
                    <Badge key={idx} variant="secondary" className="text-xs">
                      {person}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
            {entities.organizations && entities.organizations.length > 0 && (
              <div>
                <span className="text-xs font-medium text-muted-foreground">
                  Organizations
                </span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {entities.organizations.map((org, idx) => (
                    <Badge key={idx} variant="secondary" className="text-xs">
                      {org}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
            {entities.topics && entities.topics.length > 0 && (
              <div>
                <span className="text-xs font-medium text-muted-foreground">Topics</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {entities.topics.map((topic, idx) => (
                    <Badge key={idx} variant="outline" className="text-xs">
                      {topic}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Keywords Card */}
      {keywords.keywords && keywords.keywords.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <FileText className="h-5 w-5 text-primary" />
              Keywords
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {keywords.keywords.map((keyword, idx) => (
                <Badge key={idx} variant="outline">
                  {keyword}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Model Info */}
      {analysis.ai_model && (
        <div className="text-xs text-muted-foreground">
          Analyzed by: {analysis.ai_model}
          {analysis.processing_time_ms && ` (${analysis.processing_time_ms}ms)`}
        </div>
      )}
    </div>
  );
}
