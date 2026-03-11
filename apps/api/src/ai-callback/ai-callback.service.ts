import { Injectable } from '@nestjs/common';
import { AgentsService } from '../agents/agents.service';
import { WebsocketGateway } from '../websocket/websocket.gateway';

@Injectable()
export class AiCallbackService {
  constructor(
    private agentsService: AgentsService,
    private wsGateway: WebsocketGateway,
  ) {}

  async handleDecision(data: {
    agentType: string;
    symbol: string;
    signal: string;
    confidence: number;
    reasoning: string;
    metadata?: object;
  }) {
    const decision = await this.agentsService.saveDecision(data);
    this.wsGateway.broadcastAgentDecision(decision);
    return decision;
  }
}
