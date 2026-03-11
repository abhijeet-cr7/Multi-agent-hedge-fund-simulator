'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const generateMockData = (symbol: string) => {
  const data = [];
  let price = symbol === 'AAPL' ? 180 : symbol === 'NVDA' ? 650 : 400;
  const now = new Date();
  // Slight upward bias (0.51) to simulate realistic market drift
  const PRICE_DRIFT_BIAS = 0.51;

  for (let i = 29; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    price = price * (1 + (Math.random() - PRICE_DRIFT_BIAS) * 0.03);
    data.push({
      date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      price: Math.round(price * 100) / 100,
    });
  }
  return data;
};

interface StockChartProps {
  symbol: string;
}

export function StockChart({ symbol }: StockChartProps) {
  const data = generateMockData(symbol);
  const firstPrice = data[0]?.price || 0;
  const lastPrice = data[data.length - 1]?.price || 0;
  const isPositive = lastPrice >= firstPrice;
  const color = isPositive ? '#22c55e' : '#ef4444';

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>{symbol} Price History (30 Days)</span>
          <span className={isPositive ? 'text-green-500' : 'text-red-500'}>
            ${lastPrice.toFixed(2)}{' '}
            <span className="text-sm">
              ({isPositive ? '+' : ''}{(((lastPrice - firstPrice) / firstPrice) * 100).toFixed(2)}%)
            </span>
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(216 34% 17%)" />
            <XAxis
              dataKey="date"
              tick={{ fill: 'hsl(215.4 16.3% 56.9%)', fontSize: 11 }}
              tickLine={false}
              interval={6}
            />
            <YAxis
              tick={{ fill: 'hsl(215.4 16.3% 56.9%)', fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              domain={['auto', 'auto']}
              tickFormatter={(v) => `$${v.toFixed(0)}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(224 71% 8%)',
                border: '1px solid hsl(216 34% 17%)',
                borderRadius: '8px',
                color: 'hsl(213 31% 91%)',
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke={color}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: color }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
