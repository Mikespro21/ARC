import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/app/components/ui/select';
import { Label } from '@/app/components/ui/label';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

export const Analytics = () => {
  const { agents, crowdMetrics } = useApp();
  const [selectedAgentId, setSelectedAgentId] = useState('all');

  const selectedAgents = selectedAgentId === 'all' 
    ? agents 
    : agents.filter(a => a.id === selectedAgentId);

  // Portfolio distribution data
  const portfolioData = selectedAgents.map(agent => ({
    name: agent.name,
    value: agent.portfolio.totalValue,
    profit: agent.performance.totalProfit,
  }));

  // Strategy distribution
  const strategyCount = agents.reduce((acc, agent) => {
    const strategy = agent.strategy.type;
    acc[strategy] = (acc[strategy] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const strategyData = Object.entries(strategyCount).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B', '#EF4444'];

  // Performance over time (mock data)
  const performanceData = Array.from({ length: 30 }, (_, i) => {
    const data: any = { day: i + 1 };
    selectedAgents.forEach(agent => {
      data[agent.name] = 1000 + (Math.random() - 0.3) * 500 + (i * 20);
    });
    return data;
  });

  // Trade frequency data
  const tradeFrequencyData = selectedAgents.map(agent => ({
    name: agent.name,
    trades: agent.performance.totalTrades,
    avgPerDay: agent.performance.totalTrades / 30,
  }));

  // Risk vs Return scatter data
  const riskReturnData = agents.map(agent => ({
    name: agent.name,
    risk: agent.riskness,
    return: agent.performance.totalProfitPercent,
  }));

  // Win rate comparison
  const winRateData = selectedAgents.map(agent => ({
    name: agent.name,
    winRate: agent.performance.winRate,
    lossRate: 100 - agent.performance.winRate,
  }));

  // Calculate aggregate stats
  const totalValue = selectedAgents.reduce((sum, a) => sum + a.portfolio.totalValue, 0);
  const totalProfit = selectedAgents.reduce((sum, a) => sum + a.performance.totalProfit, 0);
  const avgWinRate = selectedAgents.reduce((sum, a) => sum + a.performance.winRate, 0) / (selectedAgents.length || 1);
  const totalTrades = selectedAgents.reduce((sum, a) => sum + a.performance.totalTrades, 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Analytics</h1>
        <p className="text-gray-600 mt-2">
          Detailed performance analysis and insights
        </p>
      </div>

      {/* Agent Filter */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <Label htmlFor="agent-filter" className="text-lg font-bold mb-2 block">
          Filter by Agent
        </Label>
        <Select value={selectedAgentId} onValueChange={setSelectedAgentId}>
          <SelectTrigger id="agent-filter">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Agents</SelectItem>
            {agents.map(agent => (
              <SelectItem key={agent.id} value={agent.id}>
                {agent.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-8 h-8 text-blue-600" />
            <span className="text-sm font-medium text-gray-600">Total Value</span>
          </div>
          <p className="text-3xl font-bold">${totalValue.toFixed(2)}</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            {totalProfit >= 0 ? (
              <TrendingUp className="w-8 h-8 text-green-600" />
            ) : (
              <TrendingDown className="w-8 h-8 text-red-600" />
            )}
            <span className="text-sm font-medium text-gray-600">Total P/L</span>
          </div>
          <p className={`text-3xl font-bold ${totalProfit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${totalProfit.toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-8 h-8 text-purple-600" />
            <span className="text-sm font-medium text-gray-600">Avg Win Rate</span>
          </div>
          <p className="text-3xl font-bold">{avgWinRate.toFixed(1)}%</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-8 h-8 text-orange-600" />
            <span className="text-sm font-medium text-gray-600">Total Trades</span>
          </div>
          <p className="text-3xl font-bold">{totalTrades}</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Distribution */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Portfolio Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={portfolioData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.name}: $${entry.value.toFixed(0)}`}
              >
                {portfolioData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Strategy Distribution */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Strategy Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={strategyData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {strategyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Performance Over Time */}
        <div className="bg-white rounded-xl shadow-lg p-6 lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Performance Over Time (30 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              {selectedAgents.map((agent, index) => (
                <Line
                  key={agent.id}
                  type="monotone"
                  dataKey={agent.name}
                  stroke={COLORS[index % COLORS.length]}
                  strokeWidth={2}
                  dot={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Trade Frequency */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Trade Frequency</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={tradeFrequencyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="trades" fill="#8B5CF6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Win Rate Comparison */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Win Rate Comparison</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={winRateData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Bar dataKey="winRate" fill="#10B981" name="Win Rate %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Crowd Comparison */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Crowd Comparison</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Your Avg Risk</p>
            <p className="text-2xl font-bold">
              {(selectedAgents.reduce((sum, a) => sum + a.riskness, 0) / (selectedAgents.length || 1)).toFixed(0)}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Crowd: {crowdMetrics.avgRiskness}
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Your Avg Position</p>
            <p className="text-2xl font-bold">
              {(selectedAgents.reduce((sum, a) => sum + a.settings.maxPositionSize, 0) / (selectedAgents.length || 1)).toFixed(0)}%
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Crowd: {crowdMetrics.avgPositionSize.toFixed(0)}%
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Your Avg Trades/Day</p>
            <p className="text-2xl font-bold">
              {(totalTrades / 30).toFixed(1)}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Crowd: {crowdMetrics.avgTradesPerDay.toFixed(1)}
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Crowd Size</p>
            <p className="text-2xl font-bold">{crowdMetrics.totalAgents}</p>
            <p className="text-xs text-gray-500 mt-1">Total agents</p>
          </div>
        </div>
      </div>
    </div>
  );
};
