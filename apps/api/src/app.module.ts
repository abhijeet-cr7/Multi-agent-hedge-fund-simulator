import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { StocksModule } from './stocks/stocks.module';
import { PortfolioModule } from './portfolio/portfolio.module';
import { AgentsModule } from './agents/agents.module';
import { AiCallbackModule } from './ai-callback/ai-callback.module';
import { QueueModule } from './queue/queue.module';
import { WebsocketModule } from './websocket/websocket.module';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [
    PrismaModule,
    AuthModule,
    StocksModule,
    PortfolioModule,
    AgentsModule,
    AiCallbackModule,
    QueueModule,
    WebsocketModule,
  ],
})
export class AppModule {}
