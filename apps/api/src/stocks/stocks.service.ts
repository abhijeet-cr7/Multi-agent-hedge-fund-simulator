import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class StocksService {
  constructor(private prisma: PrismaService) {}

  async getStock(symbol: string) {
    const snap = await this.prisma.stockSnapshot.findFirst({
      where: { symbol: symbol.toUpperCase() },
      orderBy: { createdAt: 'desc' },
    });
    return snap || { symbol: symbol.toUpperCase(), price: null, message: 'No data available' };
  }

  async getHistory(symbol: string, days: number = 30) {
    const since = new Date();
    since.setDate(since.getDate() - days);

    return this.prisma.stockSnapshot.findMany({
      where: { symbol: symbol.toUpperCase(), createdAt: { gte: since } },
      orderBy: { createdAt: 'asc' },
    });
  }

  async getMarketOverview() {
    const symbols = ['SPY', 'QQQ', 'DIA', 'IWM'];
    const snapshots = await Promise.all(
      symbols.map(async (s) => {
        const snap = await this.prisma.stockSnapshot.findFirst({
          where: { symbol: s },
          orderBy: { createdAt: 'desc' },
        });
        return snap || { symbol: s, price: null };
      }),
    );
    return snapshots;
  }

  async saveSnapshot(data: {
    symbol: string;
    price: number;
    open?: number;
    high?: number;
    low?: number;
    volume?: number;
    marketCap?: number;
    peRatio?: number;
  }) {
    return this.prisma.stockSnapshot.create({ data });
  }
}
