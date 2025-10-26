"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Mail } from "lucide-react";
import { formatDate, truncateText } from "@/lib/utils";

// Mock data - будет заменено на реальные данные из API
const mockEmails = [
  {
    id: 1,
    sender: "alice@example.com",
    subject: "Project Update - Q4 Review",
    preview: "Hi team, I wanted to share the latest updates on our Q4 projects...",
    date: new Date("2025-10-25T14:30:00"),
    priority: "high",
    category: "Work",
    unread: true,
  },
  {
    id: 2,
    sender: "bob@company.com",
    subject: "Meeting Tomorrow at 10 AM",
    preview: "Just a reminder about our meeting scheduled for tomorrow morning...",
    date: new Date("2025-10-25T12:15:00"),
    priority: "medium",
    category: "Work",
    unread: true,
  },
  {
    id: 3,
    sender: "newsletter@tech.com",
    subject: "Weekly Tech Digest",
    preview: "Here are this week's top stories in technology and innovation...",
    date: new Date("2025-10-24T09:00:00"),
    priority: "low",
    category: "News",
    unread: false,
  },
];

const priorityColors = {
  high: "destructive",
  medium: "warning",
  low: "secondary",
} as const;

export function MailList() {
  return (
    <div className="space-y-3">
      {mockEmails.map((email) => (
        <Card
          key={email.id}
          className={`cursor-pointer transition-all hover:shadow-md ${
            email.unread ? "border-l-4 border-l-primary" : ""
          }`}
        >
          <div className="p-4">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 space-y-1">
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{email.sender}</span>
                  {email.unread && (
                    <span className="h-2 w-2 rounded-full bg-primary"></span>
                  )}
                </div>
                <h3 className={`text-sm ${email.unread ? "font-semibold" : "font-medium"}`}>
                  {email.subject}
                </h3>
                <p className="text-xs text-muted-foreground">
                  {truncateText(email.preview, 80)}
                </p>
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className="text-xs text-muted-foreground">
                  {formatDate(email.date)}
                </span>
                <div className="flex gap-1">
                  <Badge variant={priorityColors[email.priority]} className="text-[10px]">
                    {email.priority}
                  </Badge>
                  <Badge variant="outline" className="text-[10px]">
                    {email.category}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
