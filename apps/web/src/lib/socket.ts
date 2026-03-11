'use client';

import { io, Socket } from 'socket.io-client';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:3001';

let socket: Socket | null = null;

export function getSocket(): Socket {
  if (!socket) {
    socket = io(WS_URL, { transports: ['websocket', 'polling'] });
  }
  return socket;
}

export function disconnectSocket() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
}

export type AgentDecisionEvent = {
  id: string;
  agentType: string;
  symbol: string;
  signal: string;
  confidence: number;
  reasoning: string;
  createdAt: string;
};

export type PortfolioUpdateEvent = {
  portfolioId: string;
  cash: number;
};

export type StockPriceEvent = {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
};
