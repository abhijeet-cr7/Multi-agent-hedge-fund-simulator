import { Controller, Get, Param, Query, UseGuards } from '@nestjs/common';
import { StocksService } from './stocks.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('stocks')
@UseGuards(JwtAuthGuard)
export class StocksController {
  constructor(private stocksService: StocksService) {}

  @Get('market/overview')
  getMarketOverview() {
    return this.stocksService.getMarketOverview();
  }

  @Get(':symbol')
  getStock(@Param('symbol') symbol: string) {
    return this.stocksService.getStock(symbol);
  }

  @Get(':symbol/history')
  getHistory(@Param('symbol') symbol: string, @Query('days') days?: string) {
    return this.stocksService.getHistory(symbol, days ? parseInt(days) : 30);
  }
}
