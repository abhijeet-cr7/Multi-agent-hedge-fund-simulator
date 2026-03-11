import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const mockDecisions = [
  { agentType: 'Fundamental', symbol: 'AAPL', signal: 'BUY', confidence: 0.78, createdAt: '2m ago' },
  { agentType: 'Technical', symbol: 'NVDA', signal: 'STRONG_BUY', confidence: 0.91, createdAt: '5m ago' },
  { agentType: 'Sentiment', symbol: 'MSFT', signal: 'HOLD', confidence: 0.65, createdAt: '12m ago' },
  { agentType: 'Risk', symbol: 'TSLA', signal: 'SELL', confidence: 0.72, createdAt: '18m ago' },
  { agentType: 'Portfolio Manager', symbol: 'AAPL', signal: 'BUY', confidence: 0.82, createdAt: '25m ago' },
];

const signalColor = (signal: string) => {
  if (signal === 'STRONG_BUY' || signal === 'BUY') return 'bg-green-500/20 text-green-400';
  if (signal === 'STRONG_SELL' || signal === 'SELL') return 'bg-red-500/20 text-red-400';
  return 'bg-yellow-500/20 text-yellow-400';
};

export function AgentActivityFeed() {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Agent Activity
          <span className="text-xs text-muted-foreground font-normal">Live</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {mockDecisions.map((d, i) => (
            <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium truncate">{d.agentType}</span>
                  <Badge className={signalColor(d.signal)}>{d.signal}</Badge>
                </div>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-xs text-muted-foreground">{d.symbol}</span>
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs text-muted-foreground">{Math.round(d.confidence * 100)}%</span>
                    <span className="text-xs text-muted-foreground">· {d.createdAt}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
