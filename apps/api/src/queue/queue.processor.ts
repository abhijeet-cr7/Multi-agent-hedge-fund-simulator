import { Injectable, OnModuleInit, Logger } from '@nestjs/common';
import { Worker, Job } from 'bullmq';
import axios from 'axios';

@Injectable()
export class QueueProcessor implements OnModuleInit {
  private readonly logger = new Logger(QueueProcessor.name);
  private worker: Worker;

  onModuleInit() {
    const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
    const parsed = new URL(redisUrl);

    this.worker = new Worker(
      'agent-analysis',
      async (job: Job) => {
        const { symbol, agentType } = job.data;
        this.logger.log(`Processing analysis job for ${symbol} (${agentType})`);

        const pythonAiUrl = process.env.PYTHON_AI_URL || 'http://localhost:8000';
        try {
          const response = await axios.post(`${pythonAiUrl}/analyze`, {
            symbol,
            agent_type: agentType,
          });
          this.logger.log(`Analysis complete for ${symbol}: ${JSON.stringify(response.data)}`);
          return response.data;
        } catch (err) {
          this.logger.error(`Failed to call Python AI for ${symbol}: ${err.message}`);
          throw err;
        }
      },
      {
        connection: {
          host: parsed.hostname,
          port: parseInt(parsed.port || '6379'),
        },
      },
    );

    this.worker.on('completed', (job) => {
      this.logger.log(`Job ${job.id} completed`);
    });

    this.worker.on('failed', (job, err) => {
      this.logger.error(`Job ${job?.id} failed: ${err.message}`);
    });
  }
}
