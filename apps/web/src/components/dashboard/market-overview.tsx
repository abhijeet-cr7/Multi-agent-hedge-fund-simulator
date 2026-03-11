import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const indices = [
  { name: 'S&P 500', symbol: 'SPY', price: 5234.18, change: 12.45, changePercent: 0.24 },
  { name: 'NASDAQ', symbol: 'QQQ', price: 18421.31, change: -45.22, changePercent: -0.25 },
  { name: 'DOW', symbol: 'DIA', price: 39118.86, change: 87.13, changePercent: 0.22 },
  { name: 'Russell 2000', symbol: 'IWM', price: 2042.55, change: -8.77, changePercent: -0.43 },
];

export function MarketOverview() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Market Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {indices.map((idx) => {
            const isPositive = idx.change >= 0;
            return (
              <div key={idx.symbol} className="p-4 rounded-lg bg-muted/50">
                <p className="text-xs text-muted-foreground">{idx.name}</p>
                <p className="text-lg font-bold mt-1">{idx.price.toLocaleString()}</p>
                <p className={`text-sm mt-0.5 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                  {isPositive ? '+' : ''}{idx.change.toFixed(2)} ({isPositive ? '+' : ''}{idx.changePercent.toFixed(2)}%)
                </p>
              </div>
            );
          })}
        </div>

        <div className="mt-4 p-4 rounded-lg bg-muted/30 border border-border">
          <p className="text-xs text-muted-foreground mb-2">Market Sentiment</p>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-2 rounded-full bg-border overflow-hidden">
              <div className="h-full w-3/5 rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500" />
            </div>
            <span className="text-sm font-medium text-yellow-400">Neutral</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
