import { MailList } from "@/components/mail/mail-list";
import { AnalyzerView } from "@/components/mail/analyzer-view";
import { StatsCards } from "@/components/mail/stats-cards";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to SolarMail - AI-powered email analysis
        </p>
      </div>

      <StatsCards />

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Recent Emails</h2>
          <MailList />
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">AI Analysis</h2>
          <AnalyzerView />
        </div>
      </div>
    </div>
  );
}
