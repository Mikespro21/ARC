import { useApp } from '@/app/context/AppContext';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const Dashboard = () => {
  const { user, agents, crowdMetrics } = useApp();

  const activeAgents = agents.filter(a => a.status === 'active');
  const totalPortfolioValue = agents.reduce((sum, a) => sum + a.portfolio.totalValue, 0);
  const totalProfit = agents.reduce((sum, a) => sum + a.performance.totalProfit, 0);
  const totalProfitPercent = totalPortfolioValue > 0 ? (totalProfit / (totalPortfolioValue - totalProfit)) * 100 : 0;
  const activeTrades = agents.reduce((sum, a) => sum + a.portfolio.positions.length, 0);
  const bestPerformer = agents.reduce((best, agent) => 
    agent.performance.totalProfitPercent > best.performance.totalProfitPercent ? agent : best
  , agents[0]);

  const stats = [
    { 
      label: 'Total Agents', 
      value: agents.length.toString(), 
      change: `${activeAgents.length} active`, 
      emoji: '🤖',
      positive: true,
    },
    { 
      label: 'Total Portfolio Value', 
      value: `$${totalPortfolioValue.toFixed(2)}`, 
      change: `${totalProfitPercent > 0 ? '+' : ''}${totalProfitPercent.toFixed(2)}%`, 
      emoji: '💰',
      positive: totalProfitPercent > 0,
    },
    { 
      label: 'Best Performer', 
      value: bestPerformer?.name || 'None', 
      change: bestPerformer ? `${bestPerformer.performance.totalProfitPercent > 0 ? '+' : ''}${bestPerformer.performance.totalProfitPercent.toFixed(2)}%` : '0%', 
      emoji: '🏆',
      positive: bestPerformer?.performance.totalProfitPercent > 0,
    },
    { 
      label: 'Active Positions', 
      value: activeTrades.toString(), 
      change: `${agents.reduce((sum, a) => sum + a.performance.totalTrades, 0)} total trades`, 
      emoji: '📈',
      positive: true,
    },
  ];

  // Recent activity from all agents
  const recentActivity = agents
    .flatMap(agent => 
      agent.portfolio.trades.slice(-5).map(trade => ({
        ...trade,
        agentName: agent.name,
        agentId: agent.id,
      }))
    )
    .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
    .slice(0, 5);

  // Mock performance data for chart
  const performanceData = Array.from({ length: 30 }, (_, i) => ({
    day: i + 1,
    value: 10000 + Math.random() * 3000 + (i * 100),
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <div className="text-sm text-gray-600">
          Welcome back, {user.name}!
        </div>
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">{stat.emoji}</span>
              <span className={`text-sm font-medium ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change}
              </span>
            </div>
            <h3 className="text-2xl font-bold mb-1">{stat.value}</h3>
            <p className="text-gray-600 text-sm">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Crowd Metrics */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Crowd Metrics</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-600 mb-1">Total Agents</p>
            <p className="text-2xl font-bold">{crowdMetrics.totalAgents}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Avg Risk</p>
            <p className="text-2xl font-bold">{crowdMetrics.avgRiskness}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Avg Trades/Day</p>
            <p className="text-2xl font-bold">{crowdMetrics.avgTradesPerDay.toFixed(1)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Total Volume</p>
            <p className="text-2xl font-bold">${(crowdMetrics.totalVolume / 1000).toFixed(1)}k</p>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600 mb-2">Top Strategies</p>
          <div className="flex flex-wrap gap-2">
            {crowdMetrics.topStrategies.map((strategy, idx) => (
              <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                {strategy.strategy} ({strategy.count})
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
        {recentActivity.length > 0 ? (
          <div className="space-y-4">
            {recentActivity.map((activity, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                    {activity.agentName[0]}
                  </div>
                  <div>
                    <p className="font-medium">{activity.agentName}</p>
                    <p className="text-sm text-gray-600">
                      {activity.type === 'buy' ? 'Bought' : 'Sold'} {activity.amount.toFixed(4)} {activity.symbol}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold">${activity.usdcAmount.toFixed(2)}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No recent activity. Create an agent to start trading!
          </div>
        )}
      </div>

      {/* Performance Chart */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Portfolio Performance (30 Days)</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="day" 
                stroke="#6b7280"
                tick={{ fontSize: 12 }}
                label={{ value: 'Day', position: 'insideBottom', offset: -5 }}
              />
              <YAxis 
                stroke="#6b7280"
                tick={{ fontSize: 12 }}
                label={{ value: 'Value ($)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#fff', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  padding: '8px'
                }}
                formatter={(value: number) => [`$${value.toFixed(2)}`, 'Portfolio Value']}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#8b5cf6" 
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
