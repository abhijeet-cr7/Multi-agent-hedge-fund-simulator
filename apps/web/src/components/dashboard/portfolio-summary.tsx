import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatCurrency, formatPercent } from '@/lib/utils';

const mockData = {
  totalValue: 100000,
  dailyPnl: 0,
  dailyPnlPercent: 0,
  totalPnl: 0,
  totalPnlPercent: 0,
  cash: 100000,
};

export function PortfolioSummary() {
  const isPositiveDaily = mockData.dailyPnl >= 0;
  const isPositiveTotal = mockData.totalPnl >= 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Portfolio Value</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{formatCurrency(mockData.totalValue)}</p>
          <p className={`text-sm mt-1 ${isPositiveDaily ? 'text-green-500' : 'text-red-500'}`}>
            {formatPercent(mockData.dailyPnlPercent)} today
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Daily P&amp;L</CardTitle>
        </CardHeader>
        <CardContent>
          <p className={`text-2xl font-bold ${isPositiveDaily ? 'text-green-500' : 'text-red-500'}`}>
            {formatCurrency(mockData.dailyPnl)}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            {formatPercent(mockData.dailyPnlPercent)}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Total P&amp;L</CardTitle>
        </CardHeader>
        <CardContent>
          <p className={`text-2xl font-bold ${isPositiveTotal ? 'text-green-500' : 'text-red-500'}`}>
            {formatCurrency(mockData.totalPnl)}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            {formatPercent(mockData.totalPnlPercent)} all time
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Cash Available</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{formatCurrency(mockData.cash)}</p>
          <p className="text-sm text-muted-foreground mt-1">
            {((mockData.cash / mockData.totalValue) * 100).toFixed(1)}% of portfolio
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
