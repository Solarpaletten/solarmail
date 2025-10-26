"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Mail, Inbox, Send, TrendingUp } from "lucide-react";

const stats = [
  {
    title: "Total Emails",
    value: "1,234",
    icon: Mail,
    trend: "+12%",
    color: "text-blue-500",
  },
  {
    title: "Unread",
    value: "42",
    icon: Inbox,
    trend: "-5%",
    color: "text-orange-500",
  },
  {
    title: "Sent Today",
    value: "18",
    icon: Send,
    trend: "+8%",
    color: "text-green-500",
  },
  {
    title: "AI Analyzed",
    value: "956",
    icon: TrendingUp,
    trend: "+23%",
    color: "text-purple-500",
  },
];

export function StatsCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => {
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
