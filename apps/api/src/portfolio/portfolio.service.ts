import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class PortfolioService {
  constructor(private prisma: PrismaService) {}

  async getPortfolio(userId: string) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { userId },
      include: { holdings: true },
    });
    if (!portfolio) throw new NotFoundException('Portfolio not found');
    return portfolio;
  }

  async executeTrade(
    userId: string,
    symbol: string,
    action: 'BUY' | 'SELL',
    shares: number,
    price: number,
    agentDecision?: object,
  ) {
    const portfolio = await this.prisma.portfolio.findFirst({ where: { userId } });
    if (!portfolio) throw new NotFoundException('Portfolio not found');

    const totalCost = shares * price;

    if (action === 'BUY') {
      if (portfolio.cash < totalCost) throw new BadRequestException('Insufficient cash');

      await this.prisma.portfolio.update({
        where: { id: portfolio.id },
        data: { cash: { decrement: totalCost } },
      });

      const existing = await this.prisma.holding.findUnique({
        where: { portfolioId_symbol: { portfolioId: portfolio.id, symbol: symbol.toUpperCase() } },
      });

      if (existing) {
        const newShares = existing.shares + shares;
        const newAvg = (existing.avgCostBasis * existing.shares + totalCost) / newShares;
        await this.prisma.holding.update({
          where: { id: existing.id },
          data: { shares: newShares, avgCostBasis: newAvg },
        });
      } else {
        await this.prisma.holding.create({
          data: {
            portfolioId: portfolio.id,
            symbol: symbol.toUpperCase(),
            shares,
            avgCostBasis: price,
          },
        });
      }
    } else {
      const holding = await this.prisma.holding.findUnique({
        where: { portfolioId_symbol: { portfolioId: portfolio.id, symbol: symbol.toUpperCase() } },
      });
      if (!holding || holding.shares < shares) throw new BadRequestException('Insufficient shares');

      await this.prisma.portfolio.update({
        where: { id: portfolio.id },
        data: { cash: { increment: totalCost } },
      });

      const remaining = holding.shares - shares;
      if (remaining === 0) {
        await this.prisma.holding.delete({ where: { id: holding.id } });
      } else {
        await this.prisma.holding.update({
          where: { id: holding.id },
          data: { shares: remaining },
        });
      }
    }

    return this.prisma.trade.create({
      data: {
        portfolioId: portfolio.id,
        symbol: symbol.toUpperCase(),
        action,
        shares,
        price,
        totalCost,
        agentDecision: agentDecision || null,
      },
    });
  }

  async getPerformance(userId: string) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { userId },
      include: { holdings: true, trades: { orderBy: { executedAt: 'asc' } } },
    });
    if (!portfolio) throw new NotFoundException('Portfolio not found');

    const totalInvested = portfolio.trades
      .filter((t) => t.action === 'BUY')
      .reduce((sum, t) => sum + t.totalCost, 0);

    const totalReturned = portfolio.trades
      .filter((t) => t.action === 'SELL')
      .reduce((sum, t) => sum + t.totalCost, 0);

    return {
      portfolioId: portfolio.id,
      cash: portfolio.cash,
      holdingsCount: portfolio.holdings.length,
      totalTrades: portfolio.trades.length,
      totalInvested,
      totalReturned,
      holdings: portfolio.holdings,
    };
  }
}
