import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const agents = [
  {
    type: 'Fundamental',
    description: 'Analyzes P/E ratio, EPS growth, revenue trends, profit margins, debt ratios',
    lastSignal: 'BUY',
    confidence: 0.78,
    symbol: 'AAPL',
  },
  {
    type: 'Technical',
    description: 'Analyzes RSI, MACD, Bollinger Bands, moving average crossovers',
    lastSignal: 'HOLD',
    confidence: 0.62,
    symbol: 'NVDA',
  },
  {
    type: 'Sentiment',
    description: 'Analyzes news sentiment, social media trends, analyst ratings',
    lastSignal: 'BUY',
    confidence: 0.71,
    symbol: 'MSFT',
  },
  {
    type: 'Risk',
    description: 'Calculates VaR, Sharpe ratio, max drawdown, beta, correlation analysis',
    lastSignal: 'HOLD',
    confidence: 0.55,
    symbol: 'SPY',
  },
  {
    type: 'Sector',
    description: 'Analyzes sector performance, rotation signals, relative strength',
    lastSignal: 'BUY',
    confidence: 0.69,
    symbol: 'QQQ',
  },
  {
    type: 'Portfolio Manager',
    description: 'Meta-agent: aggregates signals, weighs by confidence, applies risk constraints',
    lastSignal: 'STRONG_BUY',
    confidence: 0.82,
    symbol: 'AAPL',
  },
];

const signalColor = (signal: string) => {
  if (signal === 'STRONG_BUY' || signal === 'BUY') return 'bg-green-500/20 text-green-400';
  if (signal === 'STRONG_SELL' || signal === 'SELL') return 'bg-red-500/20 text-red-400';
  return 'bg-yellow-500/20 text-yellow-400';
};

export default function AgentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">AI Agents</h1>
        <p className="text-muted-foreground mt-1">Agent insights, decisions, and performance metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <Card key={agent.type} className="hover:border-primary/50 transition-colors">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">{agent.type}</CardTitle>
                <Badge className={signalColor(agent.lastSignal)}>{agent.lastSignal}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">{agent.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Last analyzed</span>
                  <span className="font-medium">{agent.symbol}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Confidence</span>
                  <span className="font-medium">{Math.round(agent.confidence * 100)}%</span>
                </div>
                <div className="w-full bg-border rounded-full h-2 mt-2">
                  <div
                    className="h-2 rounded-full bg-primary"
                    style={{ width: `${agent.confidence * 100}%` }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Decision History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-muted-foreground">
            <p>Run an agent analysis to see decision history here.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
