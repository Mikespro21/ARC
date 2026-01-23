import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { Trophy, Medal, TrendingUp } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/app/components/ui/tabs';

export const Leaderboards = () => {
  const { leaderboards, agents } = useApp();
  const [selectedPeriod, setSelectedPeriod] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');

  const currentLeaderboard = leaderboards[selectedPeriod];
  const myAgentBotIds = agents.map(a => a.botId);

  const getRankBadge = (rank: number) => {
    if (rank === 1) return { icon: <Trophy className="w-6 h-6" />, color: 'text-yellow-500', bg: 'bg-yellow-50' };
    if (rank === 2) return { icon: <Medal className="w-6 h-6" />, color: 'text-gray-400', bg: 'bg-gray-50' };
    if (rank === 3) return { icon: <Medal className="w-6 h-6" />, color: 'text-orange-500', bg: 'bg-orange-50' };
    return null;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Leaderboards</h1>
        <p className="text-gray-600 mt-2">
          Compare agent performance across different timeframes
        </p>
      </div>

      {/* Period Tabs */}
      <Tabs value={selectedPeriod} onValueChange={(v) => setSelectedPeriod(v as any)}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="daily">Daily</TabsTrigger>
          <TabsTrigger value="weekly">Weekly</TabsTrigger>
          <TabsTrigger value="monthly">Monthly</TabsTrigger>
          <TabsTrigger value="yearly">Yearly</TabsTrigger>
        </TabsList>

        <TabsContent value={selectedPeriod} className="mt-6">
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            {/* Top 3 Podium */}
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-8">
              <div className="flex items-end justify-center gap-4 max-w-3xl mx-auto">
                {/* 2nd Place */}
                {currentLeaderboard[1] && (
                  <div className="flex-1 text-center">
                    <div className="bg-white rounded-xl p-6 shadow-lg transform -translate-y-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-gray-300 to-gray-400 rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold text-2xl">
                        2
                      </div>
                      <p className="font-bold text-lg mb-1">{currentLeaderboard[1].botId}</p>
                      <p className="text-sm text-gray-600 mb-2">{currentLeaderboard[1].agentName}</p>
                      <p className="text-2xl font-bold text-green-600">
                        +{currentLeaderboard[1].profitPercent.toFixed(2)}%
                      </p>
                      <p className="text-sm text-gray-600">Score: {currentLeaderboard[1].score.toFixed(0)}</p>
                    </div>
                  </div>
                )}

                {/* 1st Place */}
                {currentLeaderboard[0] && (
                  <div className="flex-1 text-center">
                    <div className="bg-white rounded-xl p-6 shadow-xl">
                      <Trophy className="w-20 h-20 text-yellow-500 mx-auto mb-3" />
                      <p className="font-bold text-xl mb-1">{currentLeaderboard[0].botId}</p>
                      <p className="text-sm text-gray-600 mb-2">{currentLeaderboard[0].agentName}</p>
                      <p className="text-3xl font-bold text-green-600">
                        +{currentLeaderboard[0].profitPercent.toFixed(2)}%
                      </p>
                      <p className="text-sm text-gray-600">Score: {currentLeaderboard[0].score.toFixed(0)}</p>
                    </div>
                  </div>
                )}

                {/* 3rd Place */}
                {currentLeaderboard[2] && (
                  <div className="flex-1 text-center">
                    <div className="bg-white rounded-xl p-6 shadow-lg transform -translate-y-8">
                      <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-500 rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold text-2xl">
                        3
                      </div>
                      <p className="font-bold text-lg mb-1">{currentLeaderboard[2].botId}</p>
                      <p className="text-sm text-gray-600 mb-2">{currentLeaderboard[2].agentName}</p>
                      <p className="text-2xl font-bold text-green-600">
                        +{currentLeaderboard[2].profitPercent.toFixed(2)}%
                      </p>
                      <p className="text-sm text-gray-600">Score: {currentLeaderboard[2].score.toFixed(0)}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Full Leaderboard Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Rank</th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Bot ID</th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Agent Name</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Score</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Profit</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Profit %</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Streaks</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Trades</th>
                    <th className="px-6 py-4 text-right text-sm font-bold text-gray-700">Win Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {currentLeaderboard.map((entry) => {
                    const badge = getRankBadge(entry.rank);
                    const isMyAgent = myAgentBotIds.includes(entry.botId);

                    return (
                      <tr
                        key={entry.botId}
                        className={`border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                          isMyAgent ? 'bg-blue-50' : ''
                        }`}
                      >
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            {badge ? (
                              <div className={`w-10 h-10 ${badge.bg} rounded-full flex items-center justify-center ${badge.color}`}>
                                {badge.icon}
                              </div>
                            ) : (
                              <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center font-bold text-gray-700">
                                {entry.rank}
                              </div>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <p className="font-mono font-bold text-purple-600">{entry.botId}</p>
                        </td>
                        <td className="px-6 py-4">
                          <p className="font-medium">
                            {entry.agentName}
                            {isMyAgent && (
                              <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
                                Your Agent
                              </span>
                            )}
                          </p>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <p className="font-bold">{entry.score.toFixed(0)}</p>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <p className={`font-bold ${entry.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            ${entry.profit.toFixed(2)}
                          </p>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex items-center justify-end gap-2">
                            {entry.profitPercent >= 0 ? (
                              <TrendingUp className="w-4 h-4 text-green-600" />
                            ) : (
                              <TrendingUp className="w-4 h-4 text-red-600 rotate-180" />
                            )}
                            <span className={`font-bold ${entry.profitPercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                              {entry.profitPercent >= 0 ? '+' : ''}{entry.profitPercent.toFixed(2)}%
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <p className="text-gray-700">{entry.streaks}</p>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <p className="text-gray-700">{entry.totalTrades}</p>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <p className="text-gray-700">{entry.winRate.toFixed(0)}%</p>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Scoring Explanation */}
          <div className="bg-white rounded-xl shadow-lg p-6 mt-6">
            <h3 className="font-bold text-lg mb-3">Scoring Formula</h3>
            <div className="space-y-2 text-sm text-gray-700">
              <p>
                <strong>Score = (Profit × 100) + Streaks</strong>
              </p>
              <p>
                • Profit is rounded to 2 decimals before calculating score
              </p>
              <p>
                • Streaks = consecutive periods with profit above 0
              </p>
              <p>
                • Only bots with active status are included in rankings
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
