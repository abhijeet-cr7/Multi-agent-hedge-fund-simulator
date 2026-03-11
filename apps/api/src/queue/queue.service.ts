import { Injectable } from '@nestjs/common';
import { Queue } from 'bullmq';

@Injectable()
export class QueueService {
  private queue: Queue;

  constructor() {
    this.queue = new Queue('agent-analysis', {
      connection: {
        host: process.env.REDIS_URL
          ? new URL(process.env.REDIS_URL).hostname
          : 'localhost',
        port: process.env.REDIS_URL
          ? parseInt(new URL(process.env.REDIS_URL).port || '6379')
          : 6379,
      },
    });
  }

  async addAnalysisJob(symbol: string, agentType?: string) {
    return this.queue.add('analyze', { symbol, agentType: agentType || 'all' });
  }
}
