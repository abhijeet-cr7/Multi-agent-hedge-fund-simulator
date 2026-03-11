import { PortfolioSummary } from '@/components/dashboard/portfolio-summary';
import { MarketOverview } from '@/components/dashboard/market-overview';
import { AgentActivityFeed } from '@/components/dashboard/agent-activity-feed';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground mt-1">
          Real-time portfolio overview and AI agent activity
        </p>
      </div>

      <PortfolioSummary />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <MarketOverview />
        </div>
        <div>
          <AgentActivityFeed />
        </div>
      </div>
    </div>
  );
}
