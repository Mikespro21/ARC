import { useState } from 'react';
import { useApp } from '@/app/context/AppContext';
import { Send, Brain, Sparkles, TrendingUp, AlertTriangle, Lightbulb } from 'lucide-react';
import { Button } from '@/app/components/ui/button';
import { Textarea } from '@/app/components/ui/textarea';
import { CoachMessage } from '@/app/types';

export const Coach = () => {
  const { agents, user, crowdMetrics } = useApp();
  const [messages, setMessages] = useState<CoachMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Coach. I can help you optimize your trading strategies, analyze agent performance, and provide insights based on crowd behavior. How can I assist you today?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const generateCoachResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();

    // Strategy advice
    if (lowerMessage.includes('strategy') || lowerMessage.includes('improve') || lowerMessage.includes('better')) {
      const avgProfit = agents.reduce((sum, a) => sum + a.performance.totalProfitPercent, 0) / (agents.length || 1);
      return `Based on your current performance (avg ${avgProfit.toFixed(2)}% profit), I recommend:

1. **Diversify Risk Levels**: Your agents' risk levels vary. Consider balancing between aggressive (risk 70-100) and conservative (risk 20-40) agents.

2. **Leverage Crowd Learning**: The crowd's average risk is ${crowdMetrics.avgRiskness}. Agents closer to this tend to perform consistently.

3. **Monitor Win Rates**: Focus on agents with win rates above 55%. Consider adjusting strategies for underperformers.

4. **Position Sizing**: The crowd average is ${crowdMetrics.avgPositionSize.toFixed(0)}% per trade. Your agents should align with or slightly beat this.

Would you like specific recommendations for any particular agent?`;
    }

    // Agent-specific advice
    if (lowerMessage.includes('agent')) {
      const bestAgent = agents.reduce((best, agent) => 
        agent.performance.totalProfitPercent > best.performance.totalProfitPercent ? agent : best
      , agents[0]);

      const worstAgent = agents.reduce((worst, agent) => 
        agent.performance.totalProfitPercent < worst.performance.totalProfitPercent ? agent : worst
      , agents[0]);

      return `Agent Performance Analysis:

**Best Performer**: ${bestAgent?.name || 'N/A'}
- Profit: ${bestAgent?.performance.totalProfitPercent.toFixed(2)}%
- Strategy: ${bestAgent?.strategy.type}
- Win Rate: ${bestAgent?.performance.winRate.toFixed(0)}%

**Needs Attention**: ${worstAgent?.name || 'N/A'}
- Profit: ${worstAgent?.performance.totalProfitPercent.toFixed(2)}%
- Strategy: ${worstAgent?.strategy.type}
- Win Rate: ${worstAgent?.performance.winRate.toFixed(0)}%

**Recommendation**: Consider copying ${bestAgent?.name}'s strategy to ${worstAgent?.name}, or adjust ${worstAgent?.name}'s risk parameters.`;
    }

    // Market insights
    if (lowerMessage.includes('market') || lowerMessage.includes('buy') || lowerMessage.includes('sell')) {
      return `Market Strategy Insights:

1. **Crowd Behavior**: Currently ${crowdMetrics.totalAgents} active agents trading with average ${crowdMetrics.avgTradesPerDay.toFixed(1)} trades/day.

2. **Popular Strategies**: ${crowdMetrics.topStrategies.map(s => s.strategy).join(', ')} are most common.

3. **Risk Analysis**: Current crowd risk average is ${crowdMetrics.avgRiskness}. Higher risk agents (70+) are showing more volatility but potentially higher returns.

4. **Position Sizing**: Stay within ${crowdMetrics.avgPositionSize.toFixed(0)}% ± 10% for optimal risk-adjusted returns.

**Tip**: Paper trading allows you to test strategies without real risk. Use this to experiment!`;
    }

    // Safety and risk management
    if (lowerMessage.includes('safety') || lowerMessage.includes('risk') || lowerMessage.includes('loss')) {
      return `Safety & Risk Management Tips:

1. **Always Set Exit Triggers**: Configure max daily loss (10-15%) and max drawdown (20-30%) for each agent.

2. **Diversify**: Run multiple agents with different strategies and risk levels to spread risk.

3. **Monitor Crowd Deviation**: Agents deviating >30% from crowd metrics may face higher volatility.

4. **Auto-Approval**: Use auto-approval for routine trades, but review manually for large positions.

5. **Emergency Exits**: Keep the emergency exit option available but use sparingly.

Remember: This is paper trading with real market data, so it's perfect for learning without financial risk!`;
    }

    // Crowd learning
    if (lowerMessage.includes('crowd') || lowerMessage.includes('learn') || lowerMessage.includes('copy')) {
      return `Crowd Learning & Copy Strategies:

Crowdlike supports three copy modes:

1. **Mirror Trades**: Directly copy trades from top performers
   - Best for: Quick replication of proven strategies
   - Risk: High if copied agent fails

2. **Copy Rules**: Adopt the rules/parameters of successful agents
   - Best for: Learning strategy frameworks
   - Risk: Medium, requires adaptation

3. **Copy Strategy**: Learn from multiple agents' behavior patterns
   - Best for: Building robust, crowd-validated approaches
   - Risk: Lower, diversified learning

**Crowd Stats**:
- Total agents: ${crowdMetrics.totalAgents}
- Avg trades/day: ${crowdMetrics.avgTradesPerDay.toFixed(1)}
- Top strategies: ${crowdMetrics.topStrategies.map(s => `${s.strategy} (${s.count})`).join(', ')}

The AI decides automatically which copy mode to use based on performance data!`;
    }

    // Pricing
    if (lowerMessage.includes('price') || lowerMessage.includes('cost') || lowerMessage.includes('pay')) {
      const dailyPrice = Math.pow(agents.length, 2) * (user.settings.defaultRiskLevel / 100);
      return `Pricing Information:

**Formula**: Daily cost = (agentCount²) × (risk / 100)

**Your Current Cost**:
- Agents: ${agents.length}
- Default Risk: ${user.settings.defaultRiskLevel}
- Daily Cost: $${dailyPrice.toFixed(2)}
- Monthly Estimate: $${(dailyPrice * 30).toFixed(2)}

**Tips to Optimize**:
- Fewer agents with higher quality strategies
- Lower risk levels reduce costs
- Consolidate underperforming agents

Note: In demo mode, pricing is illustrative. Real implementation would integrate with actual payment systems.`;
    }

    // Default helpful response
    return `I can help you with:

🎯 **Strategy Optimization**: Get advice on improving your agents' performance
🤖 **Agent Analysis**: Detailed insights on your agents' strengths and weaknesses
📊 **Market Insights**: Crowd behavior and trading patterns
🛡️ **Safety Tips**: Risk management and exit strategies
📚 **Crowd Learning**: How to leverage the crowd for better results
💰 **Pricing Info**: Understanding costs and optimization

Just ask me anything! For example:
- "How can I improve my strategy?"
- "Which agent is performing best?"
- "What are the current market trends?"
- "How do I manage risk better?"`;
  };

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: CoachMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsThinking(true);

    // Simulate AI thinking delay
    setTimeout(() => {
      const response = generateCoachResponse(input);
      const assistantMessage: CoachMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsThinking(false);
    }, 1000);
  };

  const quickPrompts = [
    { icon: <TrendingUp className="w-4 h-4" />, text: 'Improve my strategy', prompt: 'How can I improve my trading strategy?' },
    { icon: <Brain className="w-4 h-4" />, text: 'Agent analysis', prompt: 'Analyze my agents performance' },
    { icon: <AlertTriangle className="w-4 h-4" />, text: 'Risk management', prompt: 'Give me safety and risk management tips' },
    { icon: <Lightbulb className="w-4 h-4" />, text: 'Market insights', prompt: 'What are the current market trends?' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Brain className="w-10 h-10 text-purple-600" />
        <div>
          <h1 className="text-4xl font-bold">AI Coach</h1>
          <p className="text-gray-600 mt-1">
            Get personalized trading advice and strategy optimization
          </p>
        </div>
      </div>

      {/* Quick Prompts */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {quickPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => {
              setInput(prompt.prompt);
            }}
            className="p-4 bg-white rounded-xl shadow hover:shadow-lg transition-shadow text-left"
          >
            <div className="flex items-center gap-2 mb-2 text-purple-600">
              {prompt.icon}
              <span className="text-sm font-medium">{prompt.text}</span>
            </div>
          </button>
        ))}
      </div>

      {/* Chat Interface */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col" style={{ height: '600px' }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.role === 'assistant' && (
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <Brain className="w-6 h-6 text-white" />
                </div>
              )}
              <div
                className={`max-w-2xl rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                <p className="text-xs mt-2 opacity-70">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
              {message.role === 'user' && (
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0 text-white font-bold">
                  {user.name[0]}
                </div>
              )}
            </div>
          ))}

          {isThinking && (
            <div className="flex gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <Brain className="w-6 h-6 text-white animate-pulse" />
              </div>
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex gap-3">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask me anything about trading strategies, agent performance, or risk management..."
              className="flex-1 min-h-[60px] max-h-[120px]"
              disabled={isThinking}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isThinking}
              className="px-6 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
};
