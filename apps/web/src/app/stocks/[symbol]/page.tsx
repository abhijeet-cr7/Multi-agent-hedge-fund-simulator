import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { StockChart } from '@/components/charts/stock-chart';

interface StockPageProps {
  params: Promise<{ symbol: string }>;
}

export default async function StockPage({ params }: StockPageProps) {
  const { symbol } = await params;

  const mockMetrics = [
    { label: 'P/E Ratio', value: '28.5' },
    { label: 'Market Cap', value: '$2.8T' },
    { label: '52w High', value: '$232.92' },
    { label: '52w Low', value: '$164.08' },
    { label: 'Volume', value: '52.3M' },
    { label: 'Avg Volume', value: '58.2M' },
  ];

  const agentSignals = [
    { agent: 'Fundamental', signal: 'BUY', confidence: 0.78 },
    { agent: 'Technical', signal: 'HOLD', confidence: 0.62 },
    { agent: 'Sentiment', signal: 'BUY', confidence: 0.71 },
    { agent: 'Risk', signal: 'HOLD', confidence: 0.55 },
    { agent: 'Sector', signal: 'BUY', confidence: 0.69 },
  ];

  const signalColor = (signal: string) => {
    if (signal === 'STRONG_BUY' || signal === 'BUY') return 'bg-green-500/20 text-green-400';
    if (signal === 'STRONG_SELL' || signal === 'SELL') return 'bg-red-500/20 text-red-400';
    return 'bg-yellow-500/20 text-yellow-400';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">{symbol.toUpperCase()}</h1>
          <p className="text-muted-foreground mt-1">Stock analysis and agent insights</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="border-green-500 text-green-400 hover:bg-green-500/10">
            Buy
          </Button>
          <Button variant="outline" className="border-red-500 text-red-400 hover:bg-red-500/10">
            Sell
          </Button>
        </div>
      </div>

      <StockChart symbol={symbol.toUpperCase()} />

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {mockMetrics.map((m) => (
          <Card key={m.label}>
            <CardContent className="pt-4 pb-4">
              <p className="text-xs text-muted-foreground">{m.label}</p>
              <p className="text-lg font-semibold mt-1">{m.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Agent Signals</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {agentSignals.map((s) => (
              <div key={s.agent} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="font-medium">{s.agent} Agent</span>
                <div className="flex items-center gap-3">
                  <div className="w-32 bg-border rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-primary"
                      style={{ width: `${s.confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-muted-foreground w-8">{Math.round(s.confidence * 100)}%</span>
                  <Badge className={signalColor(s.signal)}>{s.signal}</Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
