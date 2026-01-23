import { User, Agent, CrowdMetrics, LeaderboardEntry, AgentPerformance } from '@/app/types';

export const generateMockUser = (): User => ({
  id: 'user_1',
  name: 'Miguel',
  email: 'miguel@crowdlike.app',
  usdcBalance: 10000,
  createdAt: new Date('2024-01-01'),
  settings: {
    maxAgents: 10,
    defaultRiskLevel: 50,
    maxDeviationPercent: 30,
    notifications: true,
  },
});

export const generateMockAgents = (count: number): Agent[] => {
  const strategies: Agent['strategy']['type'][] = ['aggressive', 'conservative', 'balanced', 'swing', 'daytrading', 'hodl'];
  const names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa'];
  
  return Array.from({ length: count }, (_, i) => {
    const initialBalance = 1000 + Math.random() * 4000;
    const profit = (Math.random() - 0.3) * initialBalance * 0.3; // -30% to +70%
    const totalValue = initialBalance + profit;
    const profitPercent = (profit / initialBalance) * 100;
    
    const totalTrades = Math.floor(Math.random() * 50) + 5;
    const profitableTrades = Math.floor(totalTrades * (0.4 + Math.random() * 0.4));
    
    return {
      id: `agent_${i + 1}`,
      botId: `BOT${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      name: i < names.length ? `Agent ${names[i]}` : `Agent ${i + 1}`,
      userId: 'user_1',
      strategy: {
        type: strategies[Math.floor(Math.random() * strategies.length)],
        copyMode: Math.random() > 0.5 ? (['mirror', 'rules', 'strategy'][Math.floor(Math.random() * 3)] as any) : undefined,
      },
      riskness: Math.floor(Math.random() * 100),
      status: Math.random() > 0.1 ? 'active' : (Math.random() > 0.5 ? 'paused' : 'exited'),
      portfolio: {
        agentId: `agent_${i + 1}`,
        usdcBalance: totalValue * 0.3,
        totalValue,
        positions: generateRandomPositions(3),
        trades: [],
        lastUpdated: new Date(),
      },
      settings: {
        maxPositionSize: 15 + Math.random() * 20,
        maxTradesPerDay: 5 + Math.floor(Math.random() * 15),
        autoApprove: Math.random() > 0.3,
        safetyExits: [
          { id: '1', type: 'max_daily_loss', threshold: 5 + Math.random() * 15, enabled: true },
          { id: '2', type: 'max_drawdown', threshold: 20 + Math.random() * 20, enabled: true },
          { id: '3', type: 'fraud_alert', threshold: 0, enabled: true },
        ],
      },
      performance: {
        totalProfit: profit,
        totalProfitPercent: profitPercent,
        streaks: Math.floor(Math.random() * 10),
        winRate: (profitableTrades / totalTrades) * 100,
        totalTrades,
        profitableTrades,
        avgTradeSize: totalValue * 0.1,
        maxDrawdown: Math.random() * 20,
        sharpeRatio: 0.5 + Math.random() * 2,
        crowdDeviation: Math.random() * 40,
      },
      createdAt: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000),
      lastTradeAt: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000),
    };
  });
};

const generateRandomPositions = (count: number) => {
  const assets = [
    { id: 'bitcoin', symbol: 'BTC', price: 45000 },
    { id: 'ethereum', symbol: 'ETH', price: 2500 },
    { id: 'solana', symbol: 'SOL', price: 100 },
    { id: 'cardano', symbol: 'ADA', price: 0.5 },
    { id: 'polkadot', symbol: 'DOT', price: 7 },
  ];

  return Array.from({ length: Math.min(count, assets.length) }, (_, i) => {
    const asset = assets[i];
    const amount = Math.random() * 2;
    const averagePrice = asset.price * (0.85 + Math.random() * 0.3);
    const currentPrice = asset.price;
    const value = amount * currentPrice;
    const profitLoss = value - (amount * averagePrice);
    
    return {
      id: `pos_${i + 1}`,
      asset: asset.id,
      symbol: asset.symbol,
      amount,
      averagePrice,
      currentPrice,
      value,
      profitLoss,
      profitLossPercent: (profitLoss / (amount * averagePrice)) * 100,
      openedAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000),
    };
  });
};

export const calculateAgentPerformance = (agent: Agent): AgentPerformance => {
  const { portfolio } = agent;
  const initialValue = 2000; // Assume initial value
  const profit = portfolio.totalValue - initialValue;
  const profitPercent = (profit / initialValue) * 100;
  
  return {
    ...agent.performance,
    totalProfit: profit,
    totalProfitPercent: profitPercent,
  };
};

export const calculateCrowdMetrics = (agents: Agent[]): CrowdMetrics => {
  const activeAgents = agents.filter(a => a.status === 'active');
  
  if (activeAgents.length === 0) {
    return {
      avgRiskness: 0,
      avgTradesPerDay: 0,
      avgPositionSize: 0,
      totalAgents: 0,
      totalVolume: 0,
      topStrategies: [],
    };
  }

  const avgRiskness = activeAgents.reduce((sum, a) => sum + a.riskness, 0) / activeAgents.length;
  const avgPositionSize = activeAgents.reduce((sum, a) => sum + a.settings.maxPositionSize, 0) / activeAgents.length;
  const totalVolume = activeAgents.reduce((sum, a) => sum + a.portfolio.totalValue, 0);
  
  const strategyCount = activeAgents.reduce((acc, a) => {
    const strategy = a.strategy.type;
    acc[strategy] = (acc[strategy] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const topStrategies = Object.entries(strategyCount)
    .map(([strategy, count]) => ({ strategy, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  return {
    avgRiskness: Math.round(avgRiskness),
    avgTradesPerDay: 8.5,
    avgPositionSize: Math.round(avgPositionSize),
    totalAgents: activeAgents.length,
    totalVolume,
    topStrategies,
  };
};

export const generateLeaderboard = (
  agents: Agent[],
  period: 'daily' | 'weekly' | 'monthly' | 'yearly'
): LeaderboardEntry[] => {
  const activeAgents = agents.filter(a => a.status === 'active');
  
  return activeAgents
    .map(agent => {
      const profit = agent.performance.totalProfit;
      const profitRounded = Math.round(profit * 100) / 100;
      const score = (profitRounded * 100) + agent.performance.streaks;
      
      return {
        botId: agent.botId,
        agentName: agent.name,
        score,
        profit: profitRounded,
        profitPercent: agent.performance.totalProfitPercent,
        streaks: agent.performance.streaks,
        totalTrades: agent.performance.totalTrades,
        winRate: agent.performance.winRate,
        period,
      };
    })
    .sort((a, b) => b.score - a.score)
    .map((entry, index) => ({
      ...entry,
      rank: index + 1,
    }))
    .slice(0, 100); // Top 100
};

export const calculatePricing = (agentCount: number, riskLevel: number): number => {
  // Formula: (agentCount^2) * (risk / 100)
  return Math.pow(agentCount, 2) * (riskLevel / 100);
};

export const calculateCrowdDeviation = (agent: Agent, crowdMetrics: CrowdMetrics): number => {
  // Calculate percentile rank and deviation from crowd (50th percentile)
  const riskPercentile = Math.abs((agent.riskness / 100) * 100 - 50);
  const positionPercentile = Math.abs((agent.settings.maxPositionSize / crowdMetrics.avgPositionSize) * 50 - 50);
  const tradesPercentile = Math.abs((agent.settings.maxTradesPerDay / crowdMetrics.avgTradesPerDay) * 50 - 50);
  
  return Math.round((riskPercentile + positionPercentile + tradesPercentile) / 3);
};
