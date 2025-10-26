"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Mail, Inbox, Send, TrendingUp } from "lucide-react";
import { api } from "@/lib/api";

interface Stats {
  totalEmails: number;
  unread: number;
  sentToday: number;
  aiAnalyzed: number;
}

export function StatsCards() {
  const [stats, setStats] = useState<Stats>({
    totalEmails: 0,
    unread: 0,
    sentToday: 0,
    aiAnalyzed: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Fetch emails to calculate stats
        const emails = await api.getEmails(100);

        // Calculate basic stats
        const totalEmails = emails.length;
        const unread = 0; // Would need unread flag from API
        const sentToday = 0; // Would need sent flag from API
        const aiAnalyzed = totalEmails; // Assuming all are analyzed

        setStats({
          totalEmails,
          unread,
          sentToday,
          aiAnalyzed,
        });
      } catch (error) {
        console.error("Failed to fetch stats:", error);
        // Keep default values on error
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const statsData = [
    {
      title: "Total Emails",
      value: loading ? "..." : stats.totalEmails.toString(),
      icon: Mail,
      trend: "+12%",
      color: "text-blue-500",
    },
    {
      title: "Unread",
      value: loading ? "..." : stats.unread.toString(),
      icon: Inbox,
      trend: "-5%",
      color: "text-orange-500",
    },
    {
      title: "Sent Today",
      value: loading ? "..." : stats.sentToday.toString(),
      icon: Send,
      trend: "+8%",
      color: "text-green-500",
    },
    {
      title: "AI Analyzed",
      value: loading ? "..." : stats.aiAnalyzed.toString(),
      icon: TrendingUp,
      trend: "+23%",
      color: "text-purple-500",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {statsData.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.title}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                  <div className="flex items-baseline gap-2">
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <span className="text-xs font-medium text-green-600">{stat.trend}</span>
                  </div>
                </div>
                <div className={`rounded-lg bg-muted p-3 ${stat.color}`}>
                  <Icon className="h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
