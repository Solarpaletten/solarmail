"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Mail } from "lucide-react";
import { formatDate, truncateText } from "@/lib/utils";
import { api, Email } from "@/lib/api";
import { LoadingCard } from "@/components/ui/loading-spinner";
import { InlineError } from "@/components/ui/error-display";

const priorityColors = {
  high: "destructive",
  medium: "warning",
  low: "secondary",
} as const;

export function MailList() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEmails = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await api.getEmails(10);
      setEmails(data);
    } catch (err) {
      console.error("Failed to fetch emails:", err);
      setError(
        err instanceof Error ? err.message : "Failed to load emails. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
  }, []);

  if (loading) {
    return <LoadingCard />;
  }

  if (error) {
    return <InlineError message={error} onRetry={fetchEmails} />;
  }

  if (emails.length === 0) {
    return (
      <Card className="flex h-64 items-center justify-center">
        <div className="text-center text-muted-foreground">
          <Mail className="mx-auto mb-2 h-12 w-12 opacity-50" />
          <p>No emails found</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {emails.map((email) => (
        <Card
          key={email.id}
          className="email-card cursor-pointer"
        >
          <div className="p-4">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 space-y-1">
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{email.sender}</span>
                </div>
                <h3 className="text-sm font-semibold">{email.subject}</h3>
                <p className="text-xs text-muted-foreground">
                  {truncateText(email.body_preview || "", 80)}
                </p>
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className="text-xs text-muted-foreground">
                  {formatDate(email.date)}
                </span>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
