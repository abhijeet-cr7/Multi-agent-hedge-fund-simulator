import { Body, Controller, Get, Post, Request, UseGuards } from '@nestjs/common';
import { PortfolioService } from './portfolio.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { IsString, IsNumber, IsIn, IsPositive, IsOptional } from 'class-validator';

class TradeDto {
  @IsString()
  symbol: string;

  @IsIn(['BUY', 'SELL'])
  action: 'BUY' | 'SELL';

  @IsNumber()
  @IsPositive()
  shares: number;

  @IsNumber()
  @IsPositive()
  price: number;

  @IsOptional()
  agentDecision?: object;
}

@Controller('portfolio')
@UseGuards(JwtAuthGuard)
export class PortfolioController {
  constructor(private portfolioService: PortfolioService) {}

  @Get()
  getPortfolio(@Request() req) {
    return this.portfolioService.getPortfolio(req.user.id);
  }

  @Post('trade')
  executeTrade(@Request() req, @Body() dto: TradeDto) {
    return this.portfolioService.executeTrade(
      req.user.id,
      dto.symbol,
      dto.action,
      dto.shares,
      dto.price,
      dto.agentDecision,
    );
  }

  @Get('performance')
  getPerformance(@Request() req) {
    return this.portfolioService.getPerformance(req.user.id);
  }
}
