import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { QueueService } from '../queue/queue.service';

@Injectable()
export class AgentsService {
  constructor(
    private prisma: PrismaService,
    private queueService: QueueService,
  ) {}

  async getDecisions(limit: number = 20) {
    return this.prisma.agentDecision.findMany({
      orderBy: { createdAt: 'desc' },
      take: limit,
    });
  }

  async getDecisionsBySymbol(symbol: string) {
    return this.prisma.agentDecision.findMany({
      where: { symbol: symbol.toUpperCase() },
      orderBy: { createdAt: 'desc' },
      take: 50,
    });
  }

  async runAnalysis(symbol: string) {
    await this.queueService.addAnalysisJob(symbol.toUpperCase());
    return { status: 'queued', symbol: symbol.toUpperCase(), message: 'Analysis job enqueued' };
  }

  async saveDecision(data: {
    agentType: string;
    symbol: string;
    signal: string;
    confidence: number;
    reasoning: string;
    metadata?: object;
  }) {
    return this.prisma.agentDecision.create({ data: data as any });
  }
}
