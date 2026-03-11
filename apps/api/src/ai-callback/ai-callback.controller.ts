import { Body, Controller, Post } from '@nestjs/common';
import { AiCallbackService } from './ai-callback.service';
import { IsString, IsNumber, IsOptional, Min, Max } from 'class-validator';

class DecisionDto {
  @IsString()
  agentType: string;

  @IsString()
  symbol: string;

  @IsString()
  signal: string;

  @IsNumber()
  @Min(0)
  @Max(1)
  confidence: number;

  @IsString()
  reasoning: string;

  @IsOptional()
  metadata?: object;
}

@Controller('ai-callback')
export class AiCallbackController {
  constructor(private aiCallbackService: AiCallbackService) {}

  @Post('decision')
  handleDecision(@Body() dto: DecisionDto) {
    return this.aiCallbackService.handleDecision(dto);
  }
}
