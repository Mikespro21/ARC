# Crowdlike Quick Start Guide

Welcome to Crowdlike! This guide will help you get started in 5 minutes.

## 🚀 Installation & Setup

### Step 1: Install Dependencies
```bash
npm install
# or
pnpm install
```

### Step 2: Configure Environment (Optional)
For basic usage, the app works out of the box in demo mode. For advanced features:

```bash
cp .env.example .env
```

Edit `.env` to add your API keys (all optional):
- **CoinGecko API**: For higher rate limits on market data
- **Circle API**: For real USDC integration (future)
- **Arc/Qubic RPC**: For blockchain integration (future)

### Step 3: Run the App
```bash
npm run dev
# or
pnpm run dev
```

Open http://localhost:5173 in your browser.

## 📚 First Steps

### 1. Explore the Home Page
- Learn about Crowdlike's features
- See the getting started guide
- Understand the three core features: AI Agents, Real Market Data, Leaderboards

### 2. Check the Dashboard
- View overall portfolio statistics
- See total agents and portfolio value
- Monitor best performer
- Review recent activity
- Analyze performance charts

### 3. Create Your First Agent

**Navigate to Agents page:**
1. Click "Create Agent" button
2. Enter agent name (e.g., "Agent Alpha")
3. Choose a strategy:
   - **Aggressive**: High risk, high reward
   - **Conservative**: Safe and steady
   - **Balanced**: Best of both worlds (recommended for beginners)
   - **Swing**: Medium-term trading
   - **Day Trading**: Short-term, active
   - **HODL**: Long-term holding
4. Set riskness (0-100):
   - 0-30: Very conservative
   - 30-50: Moderate
   - 50-70: Aggressive
   - 70-100: Very aggressive
5. Allocate initial balance ($100-$10,000)
6. Click "Create Agent"

**Recommended First Agent:**
- Name: "Agent Alpha"
- Strategy: Balanced
- Riskness: 50
- Balance: $1,000

### 4. Configure Safety Settings

**Go to Safety page:**
1. Select your agent
2. Enable safety exits:
   - Max Daily Loss: 10% (recommended)
   - Max Drawdown: 25% (recommended)
   - Fraud Alert: Enabled (default)
3. Set trading limits:
   - Max Position Size: 20% (recommended)
   - Max Trades Per Day: 10 (recommended)
4. Enable Auto-Approve for convenience

### 5. Explore the Market

**Navigate to Market page:**
1. See real-time cryptocurrency prices from CoinGecko
2. Search for specific assets
3. Click "Buy" or "Sell" to execute paper trades
4. Select which agent to trade with
5. Enter amount and confirm

**Try Your First Trade:**
1. Find Bitcoin (BTC)
2. Click "Buy"
3. Select "Agent Alpha"
4. Enter 0.01 BTC
5. Execute the trade

### 6. Check the Leaderboards

**Go to Leaderboards page:**
1. Select timeframe (Daily, Weekly, Monthly, Yearly)
2. See top performers with their scores
3. Find your agents (highlighted as "Your Agent")
4. Compare performance metrics:
   - Score (formula: profit × 100 + streaks)
   - Profit %
   - Win rate
   - Total trades

### 7. Use the AI Coach

**Navigate to Coach page:**
1. Start chatting with the AI coach
2. Try quick prompts:
   - "How can I improve my strategy?"
   - "Analyze my agents performance"
   - "Give me risk management tips"
   - "What are the current market trends?"
3. Get personalized advice based on your agents' performance
4. Learn about crowd behavior and best practices

### 8. View Analytics

**Go to Analytics page:**
1. Select an agent or view all agents
2. Explore charts:
   - Portfolio distribution
   - Strategy breakdown
   - Performance over time
   - Trade frequency
   - Win rate comparison
3. Compare your performance to crowd metrics

### 9. Manage Your Profile

**Navigate to Profile page:**
1. **Profile Tab**: Update name and email
2. **Wallet Tab**: View USDC balance and agent allocations
3. **Preferences Tab**: 
   - Set max agents
   - Adjust default risk level
   - Configure crowd deviation limits
   - Enable/disable notifications
4. **Pricing Tab**: View current costs and formula
5. **Config Tab**: See environment configuration

## 💡 Tips for Success

### Strategy Tips
1. **Start Conservative**: Begin with balanced or conservative strategies
2. **Diversify**: Create multiple agents with different strategies
3. **Learn from Crowd**: Monitor crowd metrics and top performers
4. **Iterate**: Adjust risk and strategies based on performance

### Risk Management
1. **Always Use Safety Exits**: Protect against large losses
2. **Monitor Daily**: Check dashboard daily for performance
3. **Stay Within Limits**: Don't exceed recommended position sizes
4. **Test First**: Use paper trading to test strategies before real money

### Performance Optimization
1. **Track Win Rate**: Aim for >55% win rate
2. **Manage Drawdown**: Keep max drawdown under 30%
3. **Align with Crowd**: Stay within 20-30% deviation from crowd
4. **Copy Success**: Use copy modes to learn from top performers

### Learning Path
1. **Week 1**: Create 1-2 agents, learn the interface
2. **Week 2**: Experiment with different strategies
3. **Week 3**: Configure safety settings and optimize
4. **Week 4**: Use AI coach and analytics for insights
5. **Ongoing**: Monitor leaderboards and adjust strategies

## 🎯 Key Metrics to Track

### Agent Performance
- **Total Profit %**: Overall return on investment
- **Win Rate**: Percentage of profitable trades (target: >55%)
- **Streaks**: Consecutive profitable periods (higher is better)
- **Max Drawdown**: Worst peak-to-trough decline (target: <30%)
- **Crowd Deviation**: Distance from crowd average (target: <30%)

### Portfolio Health
- **Total Value**: Sum of all agent portfolios
- **USDC Balance**: Available for new agents
- **Active Positions**: Number of open trades
- **Daily P/L**: Today's profit/loss

### Crowd Comparison
- **Your vs Crowd Risk**: Compare average risk levels
- **Your vs Crowd Trades**: Compare trading frequency
- **Your vs Crowd Position Size**: Compare trade sizes
- **Strategy Distribution**: Popular strategies in the crowd

## 🔧 Troubleshooting

### Market Data Not Loading
- Check internet connection
- CoinGecko API might be rate-limited (add API key in .env)
- Try clicking "Refresh" button

### Agent Not Trading
- Check if agent status is "active" (not paused)
- Verify USDC balance is sufficient
- Check safety exits haven't been triggered
- Ensure position limits aren't exceeded

### Can't Create Agent
- Check if you've reached max agents limit
- Verify sufficient USDC balance
- Ensure minimum balance ($100) is met

### Performance Issues
- Reduce market data refresh interval in .env
- Close unused browser tabs
- Clear browser cache

## 📖 Next Steps

1. **Read the Full README**: More detailed documentation
2. **Join Community**: Connect with other Crowdlike users
3. **Experiment**: Try different strategies and risk levels
4. **Learn**: Use AI coach for continuous improvement
5. **Track Progress**: Monitor leaderboards and analytics

## 🤝 Need Help?

- **AI Coach**: Built-in assistant for immediate help
- **README.md**: Comprehensive documentation
- **GitHub Issues**: Report bugs or request features

## 🎉 Have Fun!

Remember: This is paper trading with real market data. It's a safe environment to learn trading strategies without financial risk. Experiment, learn, and enjoy the journey!

---

**Happy Trading!** 🚀📈💰
