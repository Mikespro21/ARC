// Core Types for Crowdlike

export interface User {
  id: string;
  name: string;
  email: string;
  walletAddress?: string;
  usdcBalance: number;
  createdAt: Date;
  settings: UserSettings;
}

export interface UserSettings {
  maxAgents: number;
  defaultRiskLevel: number; // 0-100
  maxDeviationPercent: number; // Max crowd deviation allowed
  notifications: boolean;
}

export interface Agent {
  id: string;
  botId: string; // Public ID for leaderboards
  name: string;
  userId: string;
  strategy: AgentStrategy;
  riskness: number; // 0-100
  status: 'active' | 'paused' | 'exited';
  portfolio: Portfolio;
  settings: AgentSettings;
  performance: AgentPerformance;
  createdAt: Date;
  lastTradeAt?: Date;
}

export interface AgentStrategy {
  type: 'aggressive' | 'conservative' | 'balanced' | 'swing' | 'daytrading' | 'hodl' | 'custom';
  copyMode?: 'mirror' | 'rules' | 'strategy'; // How this agent copies others
  copyingFromAgents?: string[]; // Agent IDs being copied
  customRules?: string;
}

export interface AgentSettings {
  maxPositionSize: number; // % of portfolio per trade
  maxTradesPerDay: number;
  allowedAssets?: string[]; // If empty, all assets allowed
  autoApprove: boolean; // Auto-approve trades within approved rules
  safetyExits: SafetyExit[];
}

export interface SafetyExit {
  id: string;
  type: 'max_daily_loss' | 'max_drawdown' | 'fraud_alert';
  threshold: number; // Percentage or value
  enabled: boolean;
  triggeredAt?: Date;
}

export interface AgentPerformance {
  totalProfit: number; // In USDC
  totalProfitPercent: number;
  streaks: number; // Consecutive profitable periods
  winRate: number; // % of profitable trades
  totalTrades: number;
  profitableTrades: number;
  avgTradeSize: number;
  maxDrawdown: number;
  sharpeRatio?: number;
  crowdDeviation: number; // Current deviation from crowd %
}

export interface Portfolio {
  agentId: string;
  usdcBalance: number;
  totalValue: number; // USDC + positions value
  positions: Position[];
  trades: Trade[];
  lastUpdated: Date;
}

export interface Position {
  id: string;
  asset: string; // e.g., "bitcoin", "ethereum"
  symbol: string; // e.g., "BTC", "ETH"
  amount: number;
  averagePrice: number;
  currentPrice: number;
  value: number; // amount * currentPrice
  profitLoss: number;
  profitLossPercent: number;
  openedAt: Date;
}

export interface Trade {
  id: string;
  agentId: string;
  asset: string;
  symbol: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number; // Last price at execution
  usdcAmount: number;
  timestamp: Date;
  reason?: string; // AI reasoning for the trade
  approved: boolean;
  executedAt?: Date;
}

export interface MarketData {
  id: string;
  symbol: string;
  name: string;
  currentPrice: number;
  priceChange24h: number;
  priceChangePercent24h: number;
  marketCap: number;
  volume24h: number;
  high24h: number;
  low24h: number;
  lastUpdated: Date;
  image?: string;
}

export interface LeaderboardEntry {
  rank: number;
  botId: string;
  agentName: string;
  score: number; // (profit * 100) + streaks
  profit: number;
  profitPercent: number;
  streaks: number;
  totalTrades: number;
  winRate: number;
  period: 'daily' | 'weekly' | 'monthly' | 'yearly';
}

export interface CrowdMetrics {
  avgRiskness: number;
  avgTradesPerDay: number;
  avgPositionSize: number;
  totalAgents: number;
  totalVolume: number;
  topStrategies: { strategy: string; count: number }[];
}

export interface PricingInfo {
  agentCount: number;
  riskLevel: number;
  dailyPrice: number; // (agentCount^2) * (risk / 100)
  monthlyEstimate: number;
}

export interface CoachMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  agentId?: string; // If asking about specific agent
}
