import { WebSocketGateway, WebSocketServer, SubscribeMessage } from '@nestjs/websockets';
import { Server } from 'socket.io';
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
@WebSocketGateway({ cors: { origin: '*' } })
export class WebsocketGateway {
  @WebSocketServer()
  server: Server;

  private readonly logger = new Logger(WebsocketGateway.name);

  broadcastAgentDecision(decision: object) {
    this.server.emit('agent:decision', decision);
  }

  broadcastPortfolioUpdate(update: object) {
    this.server.emit('portfolio:update', update);
  }

  broadcastStockPrice(data: object) {
    this.server.emit('stock:price', data);
  }

  @SubscribeMessage('subscribe:stock')
  handleSubscribeStock(client: any, symbol: string) {
    client.join(`stock:${symbol}`);
    this.logger.log(`Client ${client.id} subscribed to ${symbol}`);
  }
}
