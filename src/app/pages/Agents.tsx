import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { Plus, TrendingUp, TrendingDown, Settings, Trash2, Play, Pause, Eye } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/app/components/ui/dialog';
import { Button } from '@/app/components/ui/button';
import { Input } from '@/app/components/ui/input';
import { Label } from '@/app/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/app/components/ui/select';
import { Slider } from '@/app/components/ui/slider';
import { Agent } from '@/app/types';
import { calculatePricing } from '@/app/utils/mockData';

export const Agents = () => {
  const { user, agents, createAgent, updateAgent, deleteAgent } = useApp();
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [showDetailsDialog, setShowDetailsDialog] = useState(false);

  // Create agent form state
  const [newAgentName, setNewAgentName] = useState('');
  const [newAgentStrategy, setNewAgentStrategy] = useState<Agent['strategy']['type']>('balanced');
  const [newAgentRisk, setNewAgentRisk] = useState(50);
  const [newAgentBalance, setNewAgentBalance] = useState(1000);

  const handleCreateAgent = () => {
    if (!newAgentName.trim()) {
      alert('Please enter an agent name');
      return;
    }

    if (newAgentBalance < 100) {
      alert('Minimum initial balance is $100');
      return;
    }

    createAgent(newAgentName, { type: newAgentStrategy }, newAgentRisk, newAgentBalance);
    
    // Reset form
    setNewAgentName('');
    setNewAgentStrategy('balanced');
    setNewAgentRisk(50);
    setNewAgentBalance(1000);
    setShowCreateDialog(false);
  };

  const handleToggleStatus = (agent: Agent) => {
    const newStatus = agent.status === 'active' ? 'paused' : 'active';
    updateAgent(agent.id, { status: newStatus });
  };

  const handleDeleteAgent = (agentId: string) => {
    if (confirm('Are you sure you want to delete this agent? The balance will be returned to your account.')) {
      deleteAgent(agentId);
    }
  };

  const dailyPrice = calculatePricing(agents.length, user.settings.defaultRiskLevel);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Your Agents</h1>
          <p className="text-gray-600 mt-2">
            Managing {agents.length} agent{agents.length !== 1 ? 's' : ''} • 
            Daily cost: ${dailyPrice.toFixed(2)}
          </p>
        </div>

        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-shadow">
              <Plus className="w-5 h-5" />
              Create Agent
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Create New Agent</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 pt-4">
              <div>
                <Label htmlFor="name">Agent Name</Label>
                <Input
                  id="name"
                  value={newAgentName}
                  onChange={(e) => setNewAgentName(e.target.value)}
                  placeholder="e.g., Agent Alpha"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="strategy">Strategy Type</Label>
                <Select value={newAgentStrategy} onValueChange={(v) => setNewAgentStrategy(v as any)}>
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="aggressive">Aggressive</SelectItem>
                    <SelectItem value="conservative">Conservative</SelectItem>
                    <SelectItem value="balanced">Balanced</SelectItem>
                    <SelectItem value="swing">Swing Trading</SelectItem>
                    <SelectItem value="daytrading">Day Trading</SelectItem>
                    <SelectItem value="hodl">HODL</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="risk">Riskness: {newAgentRisk}</Label>
                <Slider
                  id="risk"
                  value={[newAgentRisk]}
                  onValueChange={(v) => setNewAgentRisk(v[0])}
                  min={0}
                  max={100}
                  step={1}
                  className="mt-2"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Higher risk = more aggressive trading
                </p>
              </div>

              <div>
                <Label htmlFor="balance">Initial Balance (USDC)</Label>
                <Input
                  id="balance"
                  type="number"
                  value={newAgentBalance}
                  onChange={(e) => setNewAgentBalance(Number(e.target.value))}
                  min={100}
                  max={user.usdcBalance}
                  className="mt-1"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Available: ${user.usdcBalance.toFixed(2)}
                </p>
              </div>

              <div className="pt-4 space-y-2">
                <Button onClick={handleCreateAgent} className="w-full">
                  Create Agent
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Agents Grid */}
      {agents.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <div className="text-6xl mb-4">🤖</div>
          <h2 className="text-2xl font-bold mb-2">No Agents Yet</h2>
          <p className="text-gray-600 mb-6">
            Create your first AI trading agent to get started
          </p>
          <Button onClick={() => setShowCreateDialog(true)} className="mx-auto">
            <Plus className="w-5 h-5 mr-2" />
            Create Your First Agent
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {agents.map((agent) => (
            <div key={agent.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                    {agent.name[0]}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">{agent.name}</h3>
                    <p className="text-sm text-gray-600">
                      {agent.strategy.type} • Risk: {agent.riskness}
                    </p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${ 
                  agent.status === 'active' 
                    ? 'bg-green-100 text-green-700' 
                    : agent.status === 'paused'
                    ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {agent.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Portfolio Value</p>
                  <p className="text-2xl font-bold">${agent.portfolio.totalValue.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Profit/Loss</p>
                  <div className="flex items-center gap-2">
                    {agent.performance.totalProfitPercent >= 0 ? (
                      <TrendingUp className="w-5 h-5 text-green-600" />
                    ) : (
                      <TrendingDown className="w-5 h-5 text-red-600" />
                    )}
                    <p className={`text-2xl font-bold ${ 
                      agent.performance.totalProfitPercent >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {agent.performance.totalProfitPercent >= 0 ? '+' : ''}
                      {agent.performance.totalProfitPercent.toFixed(2)}%
                    </p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3 text-center border-t border-gray-200 pt-4 mb-4">
                <div>
                  <p className="text-xs text-gray-600">Trades</p>
                  <p className="text-lg font-bold">{agent.performance.totalTrades}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-600">Win Rate</p>
                  <p className="text-lg font-bold">{agent.performance.winRate.toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-xs text-gray-600">Positions</p>
                  <p className="text-lg font-bold">{agent.portfolio.positions.length}</p>
                </div>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                  onClick={() => {
                    setSelectedAgent(agent);
                    setShowDetailsDialog(true);
                  }}
                >
                  <Eye className="w-4 h-4 mr-1" />
                  Details
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleToggleStatus(agent)}
                >
                  {agent.status === 'active' ? (
                    <Pause className="w-4 h-4" />
                  ) : (
                    <Play className="w-4 h-4" />
                  )}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDeleteAgent(agent.id)}
                >
                  <Trash2 className="w-4 h-4 text-red-600" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Agent Details Dialog */}
      <Dialog open={showDetailsDialog} onOpenChange={setShowDetailsDialog}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{selectedAgent?.name} Details</DialogTitle>
          </DialogHeader>
          {selectedAgent && (
            <div className="space-y-4 pt-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Bot ID</p>
                  <p className="font-mono font-bold">{selectedAgent.botId}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">USDC Balance</p>
                  <p className="font-bold">${selectedAgent.portfolio.usdcBalance.toFixed(2)}</p>
                </div>
              </div>

              <div>
                <h3 className="font-bold mb-2">Performance Metrics</h3>
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-600">Total Profit</p>
                    <p className="font-bold">${selectedAgent.performance.totalProfit.toFixed(2)}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-600">Streaks</p>
                    <p className="font-bold">{selectedAgent.performance.streaks}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-600">Max Drawdown</p>
                    <p className="font-bold">{selectedAgent.performance.maxDrawdown.toFixed(2)}%</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-600">Crowd Deviation</p>
                    <p className="font-bold">{selectedAgent.performance.crowdDeviation.toFixed(0)}%</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-bold mb-2">Current Positions ({selectedAgent.portfolio.positions.length})</h3>
                {selectedAgent.portfolio.positions.length > 0 ? (
                  <div className="space-y-2">
                    {selectedAgent.portfolio.positions.map(position => (
                      <div key={position.id} className="bg-gray-50 p-3 rounded-lg flex justify-between items-center">
                        <div>
                          <p className="font-bold">{position.symbol}</p>
                          <p className="text-sm text-gray-600">
                            {position.amount.toFixed(4)} @ ${position.averagePrice.toFixed(2)}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold">${position.value.toFixed(2)}</p>
                          <p className={`text-sm ${position.profitLossPercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {position.profitLossPercent >= 0 ? '+' : ''}{position.profitLossPercent.toFixed(2)}%
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-4">No open positions</p>
                )}
              </div>

              <div>
                <h3 className="font-bold mb-2">Safety Exits</h3>
                <div className="space-y-2">
                  {selectedAgent.settings.safetyExits.map(exit => (
                    <div key={exit.id} className="bg-gray-50 p-3 rounded-lg flex justify-between items-center">
                      <div>
                        <p className="font-medium">
                          {exit.type === 'max_daily_loss' ? 'Max Daily Loss' :
                           exit.type === 'max_drawdown' ? 'Max Drawdown' :
                           'Fraud Alert'}
                        </p>
                        <p className="text-sm text-gray-600">Threshold: {exit.threshold}%</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-sm ${
                        exit.enabled ? 'bg-green-100 text-green-700' : 'bg-gray-200 text-gray-700'
                      }`}>
                        {exit.enabled ? 'Enabled' : 'Disabled'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};
