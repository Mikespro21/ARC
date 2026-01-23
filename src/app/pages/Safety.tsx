import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/app/components/ui/select';
import { Slider } from '@/app/components/ui/slider';
import { Switch } from '@/app/components/ui/switch';
import { Button } from '@/app/components/ui/button';
import { Label } from '@/app/components/ui/label';

export const Safety = () => {
  const { agents, updateAgent } = useApp();
  const [selectedAgentId, setSelectedAgentId] = useState(agents[0]?.id || '');

  const selectedAgent = agents.find(a => a.id === selectedAgentId);

  const updateSafetyExit = (exitId: string, field: 'threshold' | 'enabled', value: number | boolean) => {
    if (!selectedAgent) return;

    const updatedExits = selectedAgent.settings.safetyExits.map(exit =>
      exit.id === exitId ? { ...exit, [field]: value } : exit
    );

    updateAgent(selectedAgent.id, {
      settings: { ...selectedAgent.settings, safetyExits: updatedExits },
    });
  };

  const triggerManualExit = () => {
    if (!selectedAgent) return;

    if (confirm(`Are you sure you want to exit all positions for ${selectedAgent.name}? All positions will be sold to USDC immediately.`)) {
      // In a real implementation, this would sell all positions
      updateAgent(selectedAgent.id, { status: 'exited' });
      alert('Emergency exit triggered. All positions have been sold to USDC.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Shield className="w-10 h-10 text-purple-600" />
        <div>
          <h1 className="text-4xl font-bold">Safety & Risk Management</h1>
          <p className="text-gray-600 mt-1">
            Configure exit triggers and safety parameters for your agents
          </p>
        </div>
      </div>

      {/* Agent Selector */}
      {agents.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <Shield className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">No Agents Yet</h2>
          <p className="text-gray-600">
            Create an agent first to configure safety settings
          </p>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <Label htmlFor="agent-select" className="text-lg font-bold mb-2 block">
              Select Agent
            </Label>
            <Select value={selectedAgentId} onValueChange={setSelectedAgentId}>
              <SelectTrigger id="agent-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {agents.map(agent => (
                  <SelectItem key={agent.id} value={agent.id}>
                    {agent.name} ({agent.status})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {selectedAgent && (
            <>
              {/* Agent Safety Overview */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Safety Status</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className={`p-4 rounded-lg ${
                    selectedAgent.status === 'active' ? 'bg-green-50' : 'bg-yellow-50'
                  }`}>
                    <div className="flex items-center gap-2 mb-2">
                      {selectedAgent.status === 'active' ? (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-yellow-600" />
                      )}
                      <p className="font-bold">Status</p>
                    </div>
                    <p className={`text-2xl font-bold ${
                      selectedAgent.status === 'active' ? 'text-green-600' : 'text-yellow-600'
                    }`}>
                      {selectedAgent.status.toUpperCase()}
                    </p>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="w-5 h-5 text-blue-600" />
                      <p className="font-bold">Risk Level</p>
                    </div>
                    <p className="text-2xl font-bold text-blue-600">
                      {selectedAgent.riskness} / 100
                    </p>
                  </div>

                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle className="w-5 h-5 text-purple-600" />
                      <p className="font-bold">Active Exits</p>
                    </div>
                    <p className="text-2xl font-bold text-purple-600">
                      {selectedAgent.settings.safetyExits.filter(e => e.enabled).length} / {selectedAgent.settings.safetyExits.length}
                    </p>
                  </div>
                </div>
              </div>

              {/* Safety Exit Configuration */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Safety Exit Triggers</h2>
                <p className="text-gray-600 mb-6">
                  When an exit is triggered, the agent will sell all positions to USDC immediately (100% exit)
                </p>

                <div className="space-y-6">
                  {selectedAgent.settings.safetyExits.map((exit) => (
                    <div key={exit.id} className="border border-gray-200 rounded-lg p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-lg font-bold mb-1">
                            {exit.type === 'max_daily_loss' ? 'Maximum Daily Loss' :
                             exit.type === 'max_drawdown' ? 'Maximum Drawdown' :
                             'Fraud/Anomaly Alert'}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {exit.type === 'max_daily_loss' ? 'Triggers when daily loss exceeds threshold' :
                             exit.type === 'max_drawdown' ? 'Triggers when drawdown from peak exceeds threshold' :
                             'Triggers on detected fraudulent or anomalous behavior'}
                          </p>
                        </div>
                        <Switch
                          checked={exit.enabled}
                          onCheckedChange={(checked) => updateSafetyExit(exit.id, 'enabled', checked)}
                        />
                      </div>

                      {exit.type !== 'fraud_alert' && (
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <Label>Threshold</Label>
                            <span className="font-bold text-purple-600">{exit.threshold}%</span>
                          </div>
                          <Slider
                            value={[exit.threshold]}
                            onValueChange={(v) => updateSafetyExit(exit.id, 'threshold', v[0])}
                            min={1}
                            max={50}
                            step={1}
                            disabled={!exit.enabled}
                            className="mb-2"
                          />
                          <p className="text-xs text-gray-500">
                            {exit.type === 'max_daily_loss' 
                              ? `Exit if daily loss exceeds ${exit.threshold}%`
                              : `Exit if drawdown exceeds ${exit.threshold}%`
                            }
                          </p>
                        </div>
                      )}

                      {exit.triggeredAt && (
                        <div className="mt-4 p-3 bg-red-50 rounded-lg flex items-center gap-2">
                          <XCircle className="w-5 h-5 text-red-600" />
                          <div>
                            <p className="font-bold text-red-600">Triggered</p>
                            <p className="text-sm text-red-600">
                              {new Date(exit.triggeredAt).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Trading Limits */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Trading Limits</h2>
                <div className="space-y-6">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <Label>Max Position Size</Label>
                      <span className="font-bold text-purple-600">
                        {selectedAgent.settings.maxPositionSize}% of portfolio
                      </span>
                    </div>
                    <Slider
                      value={[selectedAgent.settings.maxPositionSize]}
                      onValueChange={(v) => updateAgent(selectedAgent.id, {
                        settings: { ...selectedAgent.settings, maxPositionSize: v[0] }
                      })}
                      min={1}
                      max={50}
                      step={1}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Maximum % of portfolio value per single trade
                    </p>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <Label>Max Trades Per Day</Label>
                      <span className="font-bold text-purple-600">
                        {selectedAgent.settings.maxTradesPerDay} trades
                      </span>
                    </div>
                    <Slider
                      value={[selectedAgent.settings.maxTradesPerDay]}
                      onValueChange={(v) => updateAgent(selectedAgent.id, {
                        settings: { ...selectedAgent.settings, maxTradesPerDay: v[0] }
                      })}
                      min={1}
                      max={50}
                      step={1}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Maximum number of trades allowed per day
                    </p>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-bold mb-1">Auto-Approve Trades</p>
                      <p className="text-sm text-gray-600">
                        Automatically execute trades within approved rules
                      </p>
                    </div>
                    <Switch
                      checked={selectedAgent.settings.autoApprove}
                      onCheckedChange={(checked) => updateAgent(selectedAgent.id, {
                        settings: { ...selectedAgent.settings, autoApprove: checked }
                      })}
                    />
                  </div>
                </div>
              </div>

              {/* Emergency Exit */}
              <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl shadow-lg p-6 border-2 border-red-200">
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-8 h-8 text-red-600 flex-shrink-0" />
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold text-red-900 mb-2">Emergency Exit</h2>
                    <p className="text-red-700 mb-4">
                      Immediately sell all positions and convert to USDC. This action cannot be undone.
                      Use only in emergency situations.
                    </p>
                    <Button
                      onClick={triggerManualExit}
                      variant="destructive"
                      className="bg-red-600 hover:bg-red-700"
                    >
                      <XCircle className="w-5 h-5 mr-2" />
                      Trigger Emergency Exit
                    </Button>
                  </div>
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Current Performance</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Total Profit/Loss</p>
                    <p className={`text-2xl font-bold ${
                      selectedAgent.performance.totalProfit >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      ${selectedAgent.performance.totalProfit.toFixed(2)}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Max Drawdown</p>
                    <p className="text-2xl font-bold text-gray-700">
                      {selectedAgent.performance.maxDrawdown.toFixed(2)}%
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Win Rate</p>
                    <p className="text-2xl font-bold text-gray-700">
                      {selectedAgent.performance.winRate.toFixed(0)}%
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Crowd Deviation</p>
                    <p className="text-2xl font-bold text-gray-700">
                      {selectedAgent.performance.crowdDeviation.toFixed(0)}%
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};
