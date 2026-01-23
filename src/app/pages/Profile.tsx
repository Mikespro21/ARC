import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { UserCircle, Wallet, Settings, Bell, Database, Code } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/app/components/ui/tabs';
import { Input } from '@/app/components/ui/input';
import { Label } from '@/app/components/ui/label';
import { Slider } from '@/app/components/ui/slider';
import { Switch } from '@/app/components/ui/switch';
import { Button } from '@/app/components/ui/button';
import { getEnvConfigForDisplay } from '@/app/config/env';
import { calculatePricing } from '@/app/utils/mockData';

export const Profile = () => {
  const { user, agents, updateUserSettings } = useApp();
  const [name, setName] = useState(user.name);
  const [email, setEmail] = useState(user.email);
  
  const envConfig = getEnvConfigForDisplay();
  const dailyPrice = calculatePricing(agents.length, user.settings.defaultRiskLevel);

  const handleSaveProfile = () => {
    // In a real app, this would update user name/email
    alert('Profile settings saved!');
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <UserCircle className="w-10 h-10 text-purple-600" />
        <div>
          <h1 className="text-4xl font-bold">Profile & Settings</h1>
          <p className="text-gray-600 mt-1">
            Manage your account and application configuration
          </p>
        </div>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="wallet">Wallet</TabsTrigger>
          <TabsTrigger value="preferences">Preferences</TabsTrigger>
          <TabsTrigger value="pricing">Pricing</TabsTrigger>
          <TabsTrigger value="config">Config</TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-4xl font-bold">
                {user.name[0]}
              </div>
              <div>
                <h2 className="text-2xl font-bold">{user.name}</h2>
                <p className="text-gray-600">{user.email}</p>
                <p className="text-sm text-gray-500 mt-1">
                  Member since {new Date(user.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-1"
                />
              </div>

              <Button onClick={handleSaveProfile}>
                Save Profile
              </Button>
            </div>
          </div>
        </TabsContent>

        {/* Wallet Tab */}
        <TabsContent value="wallet">
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Wallet className="w-6 h-6 text-purple-600" />
                <h2 className="text-xl font-bold">USDC Balance</h2>
              </div>
              <p className="text-5xl font-bold mb-2">${user.usdcBalance.toFixed(2)}</p>
              <p className="text-sm text-gray-600">Available for agent allocation</p>
            </div>

            {user.walletAddress && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="font-bold mb-2">Connected Wallet</h3>
                <p className="font-mono text-sm bg-gray-100 p-3 rounded-lg break-all">
                  {user.walletAddress}
                </p>
              </div>
            )}

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="font-bold mb-4">Agent Allocations</h3>
              <div className="space-y-3">
                {agents.map(agent => (
                  <div key={agent.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">{agent.name}</p>
                      <p className="text-sm text-gray-600">{agent.status}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">${agent.portfolio.totalValue.toFixed(2)}</p>
                      <p className="text-sm text-gray-600">
                        USDC: ${agent.portfolio.usdcBalance.toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-blue-50 rounded-xl p-6 border-2 border-blue-200">
              <h3 className="font-bold mb-2 text-blue-900">💡 Testnet Mode</h3>
              <p className="text-sm text-blue-800">
                You're currently using testnet USDC. In production, you would connect your wallet 
                to manage real USDC on Arc/Qubic networks via Circle's embedded wallet solution.
              </p>
            </div>
          </div>
        </TabsContent>

        {/* Preferences Tab */}
        <TabsContent value="preferences">
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <Label>Max Agents</Label>
                <span className="font-bold text-purple-600">{user.settings.maxAgents}</span>
              </div>
              <Slider
                value={[user.settings.maxAgents]}
                onValueChange={(v) => updateUserSettings({ maxAgents: v[0] })}
                min={1}
                max={20}
                step={1}
              />
              <p className="text-xs text-gray-500 mt-1">
                Maximum number of agents you can create
              </p>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <Label>Default Risk Level</Label>
                <span className="font-bold text-purple-600">{user.settings.defaultRiskLevel}</span>
              </div>
              <Slider
                value={[user.settings.defaultRiskLevel]}
                onValueChange={(v) => updateUserSettings({ defaultRiskLevel: v[0] })}
                min={0}
                max={100}
                step={1}
              />
              <p className="text-xs text-gray-500 mt-1">
                Default riskness for new agents (0-100)
              </p>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <Label>Max Crowd Deviation</Label>
                <span className="font-bold text-purple-600">{user.settings.maxDeviationPercent}%</span>
              </div>
              <Slider
                value={[user.settings.maxDeviationPercent]}
                onValueChange={(v) => updateUserSettings({ maxDeviationPercent: v[0] })}
                min={0}
                max={100}
                step={5}
              />
              <p className="text-xs text-gray-500 mt-1">
                Maximum allowed deviation from crowd metrics
              </p>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p className="font-bold mb-1">Notifications</p>
                <p className="text-sm text-gray-600">
                  Receive alerts for trades, exits, and performance
                </p>
              </div>
              <Switch
                checked={user.settings.notifications}
                onCheckedChange={(checked) => updateUserSettings({ notifications: checked })}
              />
            </div>
          </div>
        </TabsContent>

        {/* Pricing Tab */}
        <TabsContent value="pricing">
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Current Pricing</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Agents</p>
                  <p className="text-3xl font-bold text-purple-600">{agents.length}</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Risk Level</p>
                  <p className="text-3xl font-bold text-purple-600">{user.settings.defaultRiskLevel}</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Daily Cost</p>
                  <p className="text-3xl font-bold text-purple-600">${dailyPrice.toFixed(2)}</p>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="font-bold mb-3">Pricing Formula</h3>
                <div className="space-y-2 text-sm">
                  <p className="font-mono bg-white p-3 rounded">
                    Daily Cost = (agentCount²) × (risk / 100)
                  </p>
                  <p className="text-gray-700">
                    <strong>Current calculation:</strong><br />
                    ({agents.length}²) × ({user.settings.defaultRiskLevel} / 100) = <strong>${dailyPrice.toFixed(2)}</strong>
                  </p>
                  <p className="text-gray-600 mt-3">
                    Monthly estimate: ${(dailyPrice * 30).toFixed(2)}
                  </p>
                  <p className="text-gray-600">
                    Yearly estimate: ${(dailyPrice * 365).toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 rounded-xl p-6 border-2 border-blue-200">
              <h3 className="font-bold mb-2 text-blue-900">💡 Demo Mode</h3>
              <p className="text-sm text-blue-800">
                Pricing is currently illustrative. In production, this would integrate with actual 
                payment systems for billing based on agent count and risk levels.
              </p>
            </div>
          </div>
        </TabsContent>

        {/* Configuration Tab */}
        <TabsContent value="config">
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Code className="w-6 h-6 text-purple-600" />
                <h2 className="text-xl font-bold">Environment Configuration</h2>
              </div>
              <p className="text-sm text-gray-600 mb-4">
                These values are configured via environment variables. Update your <code className="bg-gray-100 px-2 py-1 rounded">.env</code> file to change them.
              </p>
              <div className="space-y-2">
                {Object.entries(envConfig).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-sm">{key}</span>
                    <span className="font-mono text-sm text-gray-700 bg-white px-3 py-1 rounded">
                      {value}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="font-bold mb-4">Blockchain Configuration</h3>
              <div className="space-y-3">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="font-bold mb-1">Arc Network</p>
                  <p className="text-sm text-gray-600">Frontend layer for UI integration</p>
                  <p className="font-mono text-xs mt-2 text-gray-500">Chain ID: 1</p>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="font-bold mb-1">Qubic Network</p>
                  <p className="text-sm text-gray-600">Agent execution layer for near-instant transactions</p>
                  <p className="font-mono text-xs mt-2 text-gray-500">Chain ID: 1</p>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="font-bold mb-1">Circle + USDC</p>
                  <p className="text-sm text-gray-600">Embedded wallets for holding and moving USDC</p>
                  <p className="font-mono text-xs mt-2 text-gray-500">Contract: 0x...</p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 rounded-xl p-6 border-2 border-yellow-200">
              <h3 className="font-bold mb-2 text-yellow-900">⚠️ Environment Variables</h3>
              <p className="text-sm text-yellow-800 mb-3">
                To configure these values in production, create a <code className="bg-yellow-100 px-2 py-1 rounded">.env</code> file with:
              </p>
              <pre className="bg-yellow-900 text-yellow-100 p-4 rounded-lg text-xs overflow-x-auto">
{`# CoinGecko
VITE_COINGECKO_API_KEY=your_api_key

# Blockchain
VITE_ARC_RPC_URL=https://arc-testnet.rpc.url
VITE_QUBIC_RPC_URL=https://qubic-testnet.rpc.url

# Circle
VITE_CIRCLE_API_KEY=your_circle_key
VITE_USDC_CONTRACT_ADDRESS=0x...

# App Config
VITE_DEMO_MODE=false
VITE_TESTNET_MODE=true`}
              </pre>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
