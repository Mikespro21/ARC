import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { RefreshCw, TrendingUp, TrendingDown, Search, ShoppingCart } from 'lucide-react';
import { Button } from '@/app/components/ui/button';
import { Input } from '@/app/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/app/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/app/components/ui/select';
import { Label } from '@/app/components/ui/label';
import { MarketData } from '@/app/types';

export const Market = () => {
  const { marketData, refreshMarketData, isLoading, agents, executeTrade } = useApp();
  const [searchQuery, setSearchQuery] = useState('');
  const [showTradeDialog, setShowTradeDialog] = useState(false);
  const [selectedMarket, setSelectedMarket] = useState<MarketData | null>(null);
  const [selectedAgent, setSelectedAgent] = useState('');
  const [tradeAmount, setTradeAmount] = useState('');
  const [tradeType, setTradeType] = useState<'buy' | 'sell'>('buy');

  const filteredMarkets = marketData.filter(market =>
    market.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    market.symbol.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleTrade = () => {
    if (!selectedAgent || !selectedMarket || !tradeAmount) {
      alert('Please fill in all fields');
      return;
    }

    const amount = parseFloat(tradeAmount);
    if (isNaN(amount) || amount <= 0) {
      alert('Please enter a valid amount');
      return;
    }

    executeTrade(selectedAgent, {
      asset: selectedMarket.id,
      symbol: selectedMarket.symbol,
      type: tradeType,
      amount,
      usdcAmount: amount * selectedMarket.currentPrice,
      approved: true,
      reason: 'Manual trade from Market page',
    });

    // Reset form
    setTradeAmount('');
    setShowTradeDialog(false);
    alert(`${tradeType === 'buy' ? 'Buy' : 'Sell'} order executed successfully!`);
  };

  const openTradeDialog = (market: MarketData, type: 'buy' | 'sell') => {
    setSelectedMarket(market);
    setTradeType(type);
    setShowTradeDialog(true);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Market</h1>
          <p className="text-gray-600 mt-2">
            Real-time cryptocurrency prices from CoinGecko
          </p>
        </div>
        <Button
          onClick={refreshMarketData}
          disabled={isLoading}
          className="flex items-center gap-2"
        >
          <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <Input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search markets..."
          className="pl-10"
        />
      </div>

      {/* Market Data Table */}
      {isLoading ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-purple-600" />
          <p className="text-gray-600">Loading market data...</p>
        </div>
      ) : filteredMarkets.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <p className="text-gray-600">No markets found</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Asset</th>
                  <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Price</th>
                  <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">24h Change</th>
                  <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">24h Volume</th>
                  <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Market Cap</th>
                  <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredMarkets.map((market) => (
                  <tr key={market.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        {market.image && (
                          <img src={market.image} alt={market.name} className="w-8 h-8 rounded-full" />
                        )}
                        <div>
                          <p className="font-bold">{market.name}</p>
                          <p className="text-sm text-gray-600">{market.symbol}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <p className="font-bold">${market.currentPrice.toLocaleString()}</p>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {market.priceChangePercent24h >= 0 ? (
                          <TrendingUp className="w-4 h-4 text-green-600" />
                        ) : (
                          <TrendingDown className="w-4 h-4 text-red-600" />
                        )}
                        <span className={`font-bold ${
                          market.priceChangePercent24h >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {market.priceChangePercent24h >= 0 ? '+' : ''}
                          {market.priceChangePercent24h.toFixed(2)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <p className="text-gray-700">
                        ${(market.volume24h / 1000000).toFixed(2)}M
                      </p>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <p className="text-gray-700">
                        ${(market.marketCap / 1000000000).toFixed(2)}B
                      </p>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openTradeDialog(market, 'buy')}
                          className="text-green-600 hover:text-green-700 hover:bg-green-50"
                        >
                          Buy
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openTradeDialog(market, 'sell')}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          Sell
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Trade Dialog */}
      <Dialog open={showTradeDialog} onOpenChange={setShowTradeDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>
              {tradeType === 'buy' ? 'Buy' : 'Sell'} {selectedMarket?.name}
            </DialogTitle>
          </DialogHeader>
          {selectedMarket && (
            <div className="space-y-4 pt-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center gap-3 mb-3">
                  {selectedMarket.image && (
                    <img src={selectedMarket.image} alt={selectedMarket.name} className="w-10 h-10 rounded-full" />
                  )}
                  <div>
                    <p className="font-bold">{selectedMarket.name}</p>
                    <p className="text-sm text-gray-600">{selectedMarket.symbol}</p>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Current Price</span>
                  <span className="text-xl font-bold">${selectedMarket.currentPrice.toLocaleString()}</span>
                </div>
              </div>

              <div>
                <Label htmlFor="agent">Select Agent</Label>
                <Select value={selectedAgent} onValueChange={setSelectedAgent}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Choose an agent" />
                  </SelectTrigger>
                  <SelectContent>
                    {agents.filter(a => a.status === 'active').map(agent => (
                      <SelectItem key={agent.id} value={agent.id}>
                        {agent.name} (${agent.portfolio.usdcBalance.toFixed(2)} available)
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="amount">Amount ({selectedMarket.symbol})</Label>
                <Input
                  id="amount"
                  type="number"
                  value={tradeAmount}
                  onChange={(e) => setTradeAmount(e.target.value)}
                  placeholder="0.00"
                  step="0.0001"
                  min="0"
                  className="mt-1"
                />
                {tradeAmount && (
                  <p className="text-sm text-gray-600 mt-1">
                    Total: ${(parseFloat(tradeAmount) * selectedMarket.currentPrice).toFixed(2)} USDC
                  </p>
                )}
              </div>

              <div className="pt-4">
                <Button
                  onClick={handleTrade}
                  className={`w-full ${
                    tradeType === 'buy'
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-red-600 hover:bg-red-700'
                  }`}
                >
                  <ShoppingCart className="w-4 h-4 mr-2" />
                  {tradeType === 'buy' ? 'Execute Buy Order' : 'Execute Sell Order'}
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};
