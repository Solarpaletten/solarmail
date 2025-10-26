"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, TrendingUp, Users, FileText } from "lucide-react";

// Mock AI analysis data
const mockAnalysis = {
  sentiment: {
    type: "positive",
    score: 0.82,
    label: "Positive",
  },
  priority: {
    level: "high",
    score: 0.91,
    label: "High Priority",
  },
  category: {
    name: "Work",
    confidence: 0.88,
  },
  entities: {
    persons: ["Alice Johnson", "Bob Smith"],
    organizations: ["SolarMail Inc."],
    topics: ["Project Management", "Q4 Review"],
  },
  keywords: ["urgent", "deadline", "meeting", "update"],
};

const sentimentColors = {
  positive: "success",
  neutral: "secondary",
  negative: "destructive",
} as const;

export function AnalyzerView() {
  return (
    <div className="space-y-4">
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
              <Badge variant={sentimentColors[mockAnalysis.sentiment.type]}>
                {mockAnalysis.sentiment.label}
              </Badge>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
              <div
                className="h-full bg-green-500 transition-all"
                style={{ width: `${mockAnalysis.sentiment.score * 100}%` }}
              />
            </div>
            <span className="text-xs text-muted-foreground">
              Score: {(mockAnalysis.sentiment.score * 100).toFixed(0)}%
            </span>
          </div>

          {/* Priority */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Priority</span>
              <Badge variant="destructive">{mockAnalysis.priority.label}</Badge>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
              <div
                className="h-full bg-red-500 transition-all"
                style={{ width: `${mockAnalysis.priority.score * 100}%` }}
              />
            </div>
            <span className="text-xs text-muted-foreground">
              Score: {(mockAnalysis.priority.score * 100).toFixed(0)}%
            </span>
          </div>

          {/* Category */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Category</span>
              <Badge variant="outline">{mockAnalysis.category.name}</Badge>
            </div>
            <span className="text-xs text-muted-foreground">
              Confidence: {(mockAnalysis.category.confidence * 100).toFixed(0)}%
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Entities Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Users className="h-5 w-5 text-primary" />
            Detected Entities
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <span className="text-xs font-medium text-muted-foreground">Persons</span>
            <div className="mt-1 flex flex-wrap gap-1">
              {mockAnalysis.entities.persons.map((person) => (
                <Badge key={person} variant="secondary" className="text-xs">
                  {person}
                </Badge>
              ))}
            </div>
          </div>
          <div>
            <span className="text-xs font-medium text-muted-foreground">Organizations</span>
            <div className="mt-1 flex flex-wrap gap-1">
              {mockAnalysis.entities.organizations.map((org) => (
                <Badge key={org} variant="secondary" className="text-xs">
                  {org}
                </Badge>
              ))}
            </div>
          </div>
          <div>
            <span className="text-xs font-medium text-muted-foreground">Topics</span>
            <div className="mt-1 flex flex-wrap gap-1">
              {mockAnalysis.entities.topics.map((topic) => (
                <Badge key={topic} variant="outline" className="text-xs">
                  {topic}
                </Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Keywords Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <FileText className="h-5 w-5 text-primary" />
            Keywords
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {mockAnalysis.keywords.map((keyword) => (
              <Badge key={keyword} variant="outline">
                {keyword}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
