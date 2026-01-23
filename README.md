# Crowdlike v1.7.0

A personal finance app where AI agents trade with real market data and compare performance to improve investment outcomes.

## 🚀 Features

### Core Functionality
- **AI Trading Agents**: Create and manage multiple AI agents with different strategies
- **Real Market Data**: Integration with CoinGecko API for real-time cryptocurrency prices
- **Paper Trading**: Safe trading environment with real market data but no real money at risk
- **Crowd Learning**: Agents learn from and copy successful strategies from the crowd
- **Leaderboards**: Compare performance across daily, weekly, monthly, and yearly timeframes
- **Safety System**: Configurable exit triggers and risk management
- **Analytics**: Comprehensive performance analysis and insights
- **AI Coach**: Personalized trading advice and strategy optimization

### Technical Features
- **React + TypeScript**: Modern, type-safe frontend
- **Real-time Updates**: Market data and portfolio values update automatically
- **Responsive Design**: Works on desktop and mobile
- **Glass-morphism UI**: Beautiful gradient design with smooth animations
- **Dynamic Sidebar**: Auto-hide on scroll, mouse-reveal navigation

## 🏗️ Architecture

### Frontend Layer (Arc)
- React application for user interface
- Real-time data visualization with Recharts
- State management via React Context

### Execution Layer (Qubic)
- Near-instant transaction processing
- Agent execution environment
- Trade execution engine

### Payment Layer (Circle + USDC)
- USDC stablecoin for all transactions
- Embedded wallets via Circle
- Secure balance management

### Data Layer (CoinGecko)
- Real-time cryptocurrency prices
- Market data and trends
- Asset search and discovery

## 📊 Core Concepts

### Agents
Each agent is a full AI that can:
- Make autonomous trading decisions
- Learn from crowd behavior
- Copy strategies from top performers
- Manage its own portfolio
- Execute trades within safety limits

### Strategies
- **Aggressive**: High risk, high reward trading
- **Conservative**: Low risk, steady returns
- **Balanced**: Mix of risk and stability
- **Swing Trading**: Medium-term position trading
- **Day Trading**: Short-term, high-frequency trading
- **HODL**: Long-term holding strategy

### Copy Modes
1. **Mirror Trades**: Directly replicate trades from successful agents
2. **Copy Rules**: Adopt parameter settings and rules
3. **Copy Strategy**: Learn behavioral patterns from multiple agents

### Safety System
- **Max Daily Loss**: Auto-exit if daily loss exceeds threshold
- **Max Drawdown**: Exit on excessive drawdown from peak
- **Fraud Detection**: Anomaly detection and alerts
- **Emergency Exit**: Manual 100% position liquidation

### Scoring Formula
```
Score = (Profit × 100) + Streaks
```
- Profit is rounded to 2 decimals
- Streaks = consecutive profitable periods
- Only active agents appear on leaderboards

### Pricing Formula
```
Daily Cost = (agentCount²) × (risk / 100)
```
- Cost scales quadratically with agent count
- Risk level (0-100) acts as multiplier
- Lower risk = lower cost

### Crowd Deviation
Measures how much an agent differs from the crowd:
```
Deviation % = Avg(|percentile - 50|) across metrics
```
Metrics tracked:
- Riskness (0-100)
- Trades per day
- Position size (% of portfolio)

## 🛠️ Setup

### Prerequisites
- Node.js 18+ and npm/pnpm
- CoinGecko API key (optional, for higher rate limits)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crowdlike.git
cd crowdlike
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `VITE_COINGECKO_API_KEY`: Your CoinGecko API key
- `VITE_ARC_RPC_URL`: Arc network RPC endpoint
- `VITE_QUBIC_RPC_URL`: Qubic network RPC endpoint
- `VITE_CIRCLE_API_KEY`: Circle API key for USDC
- `VITE_DEMO_MODE`: Set to `true` for demo mode with mock data

4. Run the development server:
```bash
npm run dev
# or
pnpm run dev
```

5. Open your browser to `http://localhost:5173`

### Build for Production
```bash
npm run build
# or
pnpm run build
```

## 📖 Usage Guide

### Creating Your First Agent

1. **Navigate to Agents Page**
   - Click "Agents" in the sidebar
   - Click "Create Agent" button

2. **Configure Agent**
   - Enter a name (e.g., "Agent Alpha")
   - Choose a strategy type
   - Set riskness level (0-100)
   - Allocate initial USDC balance

3. **Monitor Performance**
   - View agent portfolio on Dashboard
   - Check positions and trades
   - Monitor profit/loss in real-time

### Setting Up Safety Exits

1. **Go to Safety Page**
   - Select your agent
   - Configure exit triggers:
     - Max Daily Loss (recommended: 10-15%)
     - Max Drawdown (recommended: 20-30%)
     - Fraud Alert (enabled by default)

2. **Set Trading Limits**
   - Max Position Size (% of portfolio)
   - Max Trades Per Day
   - Auto-approve within limits

### Using the AI Coach

1. **Navigate to Coach Page**
2. **Ask Questions** like:
   - "How can I improve my strategy?"
   - "Which agent is performing best?"
   - "What are the current market trends?"
   - "Give me risk management tips"

3. **Use Quick Prompts** for common queries

### Trading in the Market

1. **Go to Market Page**
2. **Browse Real-Time Prices** from CoinGecko
3. **Execute Trades**:
   - Click Buy/Sell on any asset
   - Select which agent to trade with
   - Enter amount
   - Confirm execution

### Viewing Analytics

1. **Navigate to Analytics Page**
2. **Select Agent** or view all agents
3. **Explore Charts**:
   - Portfolio distribution
   - Strategy breakdown
   - Performance over time
   - Win rate comparison
   - Risk vs return analysis

### Checking Leaderboards

1. **Go to Leaderboards Page**
2. **Select Timeframe**: Daily, Weekly, Monthly, or Yearly
3. **Find Your Agents**: Highlighted with "Your Agent" badge
4. **View Rankings**: Top performers with scores and stats

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- **VITE_DEMO_MODE**: Enable/disable demo mode (default: true)
- **VITE_TESTNET_MODE**: Use testnet or mainnet (default: true)
- **VITE_MARKET_REFRESH_INTERVAL**: Market data update interval in ms (default: 30000)
- **VITE_MAX_AGENTS**: Maximum agents per user (default: 10)

### User Preferences

Configurable in Profile > Preferences:
- Max Agents
- Default Risk Level
- Max Crowd Deviation
- Notifications

## 🧪 Demo Mode

When `VITE_DEMO_MODE=true`:
- Uses mock data for agents and trades
- CoinGecko API provides real market prices
- No real blockchain transactions
- Perfect for learning and testing

## 🔐 Security Notes

- **Paper Trading Only**: Currently implements paper trading
- **No Real Money**: No actual funds at risk
- **Educational Purpose**: Designed for learning trading strategies
- **Testnet**: Use testnet mode for blockchain integration testing

## 🎨 UI/UX Features

- **Dynamic Sidebar**: 
  - Hover left edge to reveal
  - Move right to hide
  - Auto-hides on scroll down
  - Search functionality

- **Glass-morphism Design**:
  - Gradient background (blue → white → purple)
  - Frosted glass effects
  - Smooth animations
  - Premium feel

- **Responsive Layout**:
  - Works on desktop and mobile
  - Adaptive grid layouts
  - Touch-friendly controls

## 📈 Roadmap

### Current (v1.7.0)
- ✅ Full agent management
- ✅ Real market data integration
- ✅ Paper trading system
- ✅ Leaderboards and analytics
- ✅ Safety and risk management
- ✅ AI Coach

### Future Enhancements
- 🔄 Real blockchain integration (Arc + Qubic)
- 🔄 Actual USDC transactions via Circle
- 🔄 Advanced AI agent strategies
- 🔄 Social features (agent sharing, following)
- 🔄 Mobile app (React Native)
- 🔄 Historical backtesting
- 🔄 Advanced chart indicators

## 🤝 Contributing

This is Miguel's personal project for learning. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Miguel** - Age 13, Building Crowdlike to learn programming, math, and finance

Target completion: ~3 years

## 🙏 Acknowledgments

- CoinGecko for market data API
- Arc Network for frontend layer
- Qubic Network for execution layer
- Circle for USDC integration
- Figma Make for development environment

---

**Version**: 1.7.0  
**Last Updated**: January 23, 2026  
**Status**: Active Development 🚀
