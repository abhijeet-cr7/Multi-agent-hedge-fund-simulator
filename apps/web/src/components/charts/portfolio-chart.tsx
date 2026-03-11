'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';

const performanceData = Array.from({ length: 30 }, (_, i) => ({
  date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  }),
  value: 100000 + Math.random() * 5000 - 2000,
}));

const allocationData = [
  { name: 'Cash', value: 100, color: '#64748b' },
];

interface PortfolioChartProps {
  type: 'performance' | 'allocation';
}

export function PortfolioChart({ type }: PortfolioChartProps) {
  if (type === 'allocation') {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio Allocation</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={allocationData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={4}
                dataKey="value"
              >
                {allocationData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(224 71% 8%)',
                  border: '1px solid hsl(216 34% 17%)',
                  borderRadius: '8px',
                  color: 'hsl(213 31% 91%)',
                }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Portfolio Performance</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={performanceData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(210 40% 98%)" stopOpacity={0.15} />
                <stop offset="95%" stopColor="hsl(210 40% 98%)" stopOpacity={0} />
              </linearGradient>
            </defs>
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
              tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(224 71% 8%)',
                border: '1px solid hsl(216 34% 17%)',
                borderRadius: '8px',
                color: 'hsl(213 31% 91%)',
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, 'Portfolio Value']}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="hsl(210 40% 98%)"
              strokeWidth={2}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
