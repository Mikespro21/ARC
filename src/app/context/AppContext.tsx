import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, Agent, MarketData, CrowdMetrics, LeaderboardEntry, Trade } from '@/app/types';
import { coinGeckoService } from '@/app/services/coinGeckoService';
import { ENV_CONFIG } from '@/app/config/env';
import { generateMockAgents, generateMockUser, calculateAgentPerformance, calculateCrowdMetrics, generateLeaderboard } from '@/app/utils/mockData';

interface AppContextType {
  user: User;
  agents: Agent[];
  marketData: MarketData[];
  crowdMetrics: CrowdMetrics;
  leaderboards: {
    daily: LeaderboardEntry[];
    weekly: LeaderboardEntry[];
    monthly: LeaderboardEntry[];
    yearly: LeaderboardEntry[];
  };
  isLoading: boolean;
  
  // Actions
  createAgent: (name: string, strategy: Agent['strategy'], riskness: number, initialBalance: number) => void;
  updateAgent: (agentId: string, updates: Partial<Agent>) => void;
  deleteAgent: (agentId: string) => void;
  executeTrade: (agentId: string, trade: Omit<Trade, 'id' | 'timestamp' | 'agentId'>) => void;
  refreshMarketData: () => Promise<void>;
  updateUserSettings: (settings: Partial<User['settings']>) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider = ({ children }: AppProviderProps) => {
  const [user, setUser] = useState<User>(generateMockUser());
  const [agents, setAgents] = useState<Agent[]>(generateMockAgents(4));
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [crowdMetrics, setCrowdMetrics] = useState<CrowdMetrics>(calculateCrowdMetrics(generateMockAgents(100)));
  const [leaderboards, setLeaderboards] = useState({
    daily: [] as LeaderboardEntry[],
    weekly: [] as LeaderboardEntry[],
    monthly: [] as LeaderboardEntry[],
    yearly: [] as LeaderboardEntry[],
  });
  const [isLoading, setIsLoading] = useState(true);

  // Fetch market data on mount and periodically
  useEffect(() => {
    const fetchMarketData = async () => {
      try {
        const data = await coinGeckoService.getMarketData([
          'bitcoin',
          'ethereum',
          'solana',
          'cardano',
          'polkadot',
          'binancecoin',
          'ripple',
          'dogecoin',
        ]);
        setMarketData(data);
      } catch (error) {
        console.error('Error fetching market data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMarketData();
    const interval = setInterval(fetchMarketData, ENV_CONFIG.MARKET_DATA_REFRESH_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);

  // Update leaderboards when agents change
  useEffect(() => {
    const allAgents = [...agents, ...generateMockAgents(96)]; // Add more for crowd
    setLeaderboards({
      daily: generateLeaderboard(allAgents, 'daily'),
      weekly: generateLeaderboard(allAgents, 'weekly'),
      monthly: generateLeaderboard(allAgents, 'monthly'),
      yearly: generateLeaderboard(allAgents, 'yearly'),
    });
    setCrowdMetrics(calculateCrowdMetrics(allAgents));
  }, [agents]);

  // Update agent portfolio values based on market data
  useEffect(() => {
    if (marketData.length === 0) return;

    setAgents(prevAgents => {
      return prevAgents.map(agent => {
        const updatedPositions = agent.portfolio.positions.map(position => {
          const market = marketData.find(m => m.id === position.asset);
          if (market) {
            const currentPrice = market.currentPrice;
            const value = position.amount * currentPrice;
            const profitLoss = value - (position.amount * position.averagePrice);
            const profitLossPercent = (profitLoss / (position.amount * position.averagePrice)) * 100;

            return {
              ...position,
              currentPrice,
              value,
              profitLoss,
              profitLossPercent,
            };
          }
          return position;
        });

        const totalPositionValue = updatedPositions.reduce((sum, p) => sum + p.value, 0);
        const totalValue = agent.portfolio.usdcBalance + totalPositionValue;

        return {
          ...agent,
          portfolio: {
            ...agent.portfolio,
            positions: updatedPositions,
            totalValue,
            lastUpdated: new Date(),
          },
          performance: calculateAgentPerformance({
            ...agent,
            portfolio: {
              ...agent.portfolio,
              positions: updatedPositions,
              totalValue,
            },
          }),
        };
      });
    });
  }, [marketData]);

  const createAgent = (name: string, strategy: Agent['strategy'], riskness: number, initialBalance: number) => {
    if (agents.length >= ENV_CONFIG.MAX_AGENTS_PER_USER) {
      alert(`Maximum ${ENV_CONFIG.MAX_AGENTS_PER_USER} agents allowed`);
      return;
    }

    if (user.usdcBalance < initialBalance) {
      alert('Insufficient USDC balance');
      return;
    }

    const newAgent: Agent = {
      id: `agent_${Date.now()}`,
      botId: `BOT${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      name,
      userId: user.id,
      strategy,
      riskness,
      status: 'active',
      portfolio: {
        agentId: '',
        usdcBalance: initialBalance,
        totalValue: initialBalance,
        positions: [],
        trades: [],
        lastUpdated: new Date(),
      },
      settings: {
        maxPositionSize: 20,
        maxTradesPerDay: 10,
        autoApprove: true,
        safetyExits: [
          { id: '1', type: 'max_daily_loss', threshold: 10, enabled: true },
          { id: '2', type: 'max_drawdown', threshold: 25, enabled: true },
          { id: '3', type: 'fraud_alert', threshold: 0, enabled: true },
        ],
      },
      performance: {
        totalProfit: 0,
        totalProfitPercent: 0,
        streaks: 0,
        winRate: 0,
        totalTrades: 0,
        profitableTrades: 0,
        avgTradeSize: 0,
        maxDrawdown: 0,
        crowdDeviation: 0,
      },
      createdAt: new Date(),
    };

    newAgent.portfolio.agentId = newAgent.id;

    setAgents(prev => [...prev, newAgent]);
    setUser(prev => ({ ...prev, usdcBalance: prev.usdcBalance - initialBalance }));
  };

  const updateAgent = (agentId: string, updates: Partial<Agent>) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId ? { ...agent, ...updates } : agent
    ));
  };

  const deleteAgent = (agentId: string) => {
    const agent = agents.find(a => a.id === agentId);
    if (agent) {
      // Return balance to user
      setUser(prev => ({ ...prev, usdcBalance: prev.usdcBalance + agent.portfolio.totalValue }));
      setAgents(prev => prev.filter(a => a.id !== agentId));
    }
  };

  const executeTrade = async (agentId: string, trade: Omit<Trade, 'id' | 'timestamp' | 'agentId'>) => {
    const agent = agents.find(a => a.id === agentId);
    if (!agent) return;

    // Get current price
    const price = await coinGeckoService.getPrice(trade.asset);
    
    const newTrade: Trade = {
      ...trade,
      id: `trade_${Date.now()}`,
      agentId,
      price,
      timestamp: new Date(),
      executedAt: new Date(),
    };

    setAgents(prev => prev.map(a => {
      if (a.id !== agentId) return a;

      const portfolio = { ...a.portfolio };
      
      if (trade.type === 'buy') {
        const cost = trade.amount * price;
        if (cost > portfolio.usdcBalance) {
          alert('Insufficient USDC balance');
          return a;
        }

        portfolio.usdcBalance -= cost;
        
        const existingPosition = portfolio.positions.find(p => p.asset === trade.asset);
        if (existingPosition) {
          const totalAmount = existingPosition.amount + trade.amount;
          const totalCost = (existingPosition.amount * existingPosition.averagePrice) + cost;
          existingPosition.amount = totalAmount;
          existingPosition.averagePrice = totalCost / totalAmount;
          existingPosition.currentPrice = price;
          existingPosition.value = totalAmount * price;
        } else {
          portfolio.positions.push({
            id: `pos_${Date.now()}`,
            asset: trade.asset,
            symbol: trade.symbol,
            amount: trade.amount,
            averagePrice: price,
            currentPrice: price,
            value: trade.amount * price,
            profitLoss: 0,
            profitLossPercent: 0,
            openedAt: new Date(),
          });
        }
      } else {
        // Sell
        const position = portfolio.positions.find(p => p.asset === trade.asset);
        if (!position || position.amount < trade.amount) {
          alert('Insufficient position size');
          return a;
        }

        const saleValue = trade.amount * price;
        portfolio.usdcBalance += saleValue;

        if (position.amount === trade.amount) {
          portfolio.positions = portfolio.positions.filter(p => p.asset !== trade.asset);
        } else {
          position.amount -= trade.amount;
          position.value = position.amount * price;
        }
      }

      portfolio.trades.push(newTrade);
      portfolio.totalValue = portfolio.usdcBalance + 
        portfolio.positions.reduce((sum, p) => sum + p.value, 0);

      return {
        ...a,
        portfolio,
        lastTradeAt: new Date(),
        performance: calculateAgentPerformance({ ...a, portfolio }),
      };
    }));
  };

  const refreshMarketData = async () => {
    setIsLoading(true);
    try {
      const data = await coinGeckoService.getMarketData();
      setMarketData(data);
    } finally {
      setIsLoading(false);
    }
  };

  const updateUserSettings = (settings: Partial<User['settings']>) => {
    setUser(prev => ({
      ...prev,
      settings: { ...prev.settings, ...settings },
    }));
  };

  return (
    <AppContext.Provider
      value={{
        user,
        agents,
        marketData,
        crowdMetrics,
        leaderboards,
        isLoading,
        createAgent,
        updateAgent,
        deleteAgent,
        executeTrade,
        refreshMarketData,
        updateUserSettings,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};