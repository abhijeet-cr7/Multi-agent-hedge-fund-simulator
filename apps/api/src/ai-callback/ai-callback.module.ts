import { Module } from '@nestjs/common';
import { AiCallbackController } from './ai-callback.controller';
import { AiCallbackService } from './ai-callback.service';
import { AgentsModule } from '../agents/agents.module';
import { WebsocketModule } from '../websocket/websocket.module';

@Module({
  imports: [AgentsModule, WebsocketModule],
  controllers: [AiCallbackController],
  providers: [AiCallbackService],
})
export class AiCallbackModule {}
