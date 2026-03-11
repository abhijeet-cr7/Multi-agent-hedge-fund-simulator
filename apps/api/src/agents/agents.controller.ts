import { Body, Controller, Get, Param, Post, Query, UseGuards } from '@nestjs/common';
import { AgentsService } from './agents.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { IsString } from 'class-validator';

class RunAnalysisDto {
  @IsString()
  symbol: string;
}

@Controller('agents')
@UseGuards(JwtAuthGuard)
export class AgentsController {
  constructor(private agentsService: AgentsService) {}

  @Get('decisions')
  getDecisions(@Query('limit') limit?: string) {
    return this.agentsService.getDecisions(limit ? parseInt(limit) : 20);
  }

  @Get('decisions/:symbol')
  getDecisionsBySymbol(@Param('symbol') symbol: string) {
    return this.agentsService.getDecisionsBySymbol(symbol);
  }

  @Post('run')
  runAnalysis(@Body() dto: RunAnalysisDto) {
    return this.agentsService.runAnalysis(dto.symbol);
  }
}
