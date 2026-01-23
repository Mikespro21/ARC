from __future__ import annotations

import random
import datetime as dt
from dataclasses import dataclass, field
from typing import Literal, Optional, List

StrategyType = Literal["aggressive","conservative","balanced","swing","daytrading","hodl","custom"]
AgentStatus = Literal["active","paused","exited"]

@dataclass
class UserSettings:
    maxAgents: int = 10
    defaultRiskLevel: int = 50
    maxDeviationPercent: int = 30
    notifications: bool = True

@dataclass
class User:
    id: str
    name: str
    email: str
    usdcBalance: float
    createdAt: dt.datetime
    settings: UserSettings = field(default_factory=UserSettings)

@dataclass
class SafetyExit:
    id: str
    type: Literal["max_daily_loss","max_drawdown","fraud_alert"]
    threshold: float
    enabled: bool = True
    triggeredAt: Optional[dt.datetime] = None

@dataclass
class AgentPerformance:
    totalProfit: float
    totalProfitPercent: float
    streaks: int
    winRate: float
    totalTrades: int
    profitableTrades: int
    avgTradeSize: float
    maxDrawdown: float
    crowdDeviation: float

@dataclass
class Position:
    symbol: str
    amount: float
    entryPrice: float
    currentPrice: float

    @property
    def value(self) -> float:
        return self.amount * self.currentPrice

@dataclass
class Trade:
    id: str
    agentId: str
    symbol: str
    side: Literal["buy","sell"]
    amount: float
    price: float
    timestamp: dt.datetime

@dataclass
class AgentSettings:
    maxPositionSize: float
    maxTradesPerDay: int
    autoApprove: bool
    safetyExits: List[SafetyExit]

@dataclass
class Portfolio:
    agentId: str
    usdcBalance: float
    totalValue: float
    positions: List[Position]
    trades: List[Trade]
    lastUpdated: dt.datetime

@dataclass
class AgentStrategy:
    type: StrategyType
    copyMode: Optional[Literal["mirror","rules","strategy"]] = None

@dataclass
class Agent:
    id: str
    botId: str
    name: str
    userId: str
    strategy: AgentStrategy
    riskness: int
    status: AgentStatus
    portfolio: Portfolio
    settings: AgentSettings
    performance: AgentPerformance
    createdAt: dt.datetime
    lastTradeAt: Optional[dt.datetime] = None

@dataclass
class CrowdMetrics:
    avgRiskness: int
    avgPositionSize: float
    avgWinRate: float
    momentumScore: float
    strainScore: float
    similarityScore: float

@dataclass
class LeaderboardEntry:
    rank: int
    botId: str
    name: str
    profitPercent: float
    winRate: float
    riskness: int

DEFAULT_ASSETS = [
    ("BTC","bitcoin"),
    ("ETH","ethereum"),
    ("SOL","solana"),
    ("ADA","cardano"),
    ("DOT","polkadot"),
    ("BNB","binancecoin"),
    ("XRP","ripple"),
    ("DOGE","dogecoin"),
]

def generate_mock_user() -> User:
    return User(
        id="user_1",
        name="Miguel",
        email="miguel@crowdlike.app",
        usdcBalance=10_000.0,
        createdAt=dt.datetime(2024,1,1),
        settings=UserSettings(maxAgents=10, defaultRiskLevel=50, maxDeviationPercent=30, notifications=True),
    )

def _rand_bot_id() -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "BOT" + "".join(random.choice(alphabet) for _ in range(6))

def _random_positions(n: int = 3) -> List[Position]:
    picks = random.sample(DEFAULT_ASSETS, k=min(n, len(DEFAULT_ASSETS)))
    positions: List[Position] = []
    for sym, _ in picks:
        entry = random.uniform(10, 200)
        current = entry * random.uniform(0.85, 1.25)
        amount = random.uniform(0.2, 3.0)
        positions.append(Position(symbol=sym, amount=amount, entryPrice=entry, currentPrice=current))
    return positions

def generate_mock_agents(count: int = 4, user_id: str = "user_1") -> List[Agent]:
    strategies: List[StrategyType] = ["aggressive","conservative","balanced","swing","daytrading","hodl"]
    names = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta","Iota","Kappa"]

    agents: List[Agent] = []
    now = dt.datetime.now()

    for i in range(count):
        initial_balance = 1000 + random.random()*4000
        profit = (random.random() - 0.3) * initial_balance * 0.3
        total_value = initial_balance + profit
        profit_pct = (profit / initial_balance) * 100

        total_trades = random.randint(5, 55)
        profitable_trades = int(total_trades * (0.4 + random.random() * 0.4))
        win_rate = (profitable_trades / total_trades) * 100

        positions = _random_positions(3)
        usdc_balance = total_value * 0.3

        perf = AgentPerformance(
            totalProfit=profit,
            totalProfitPercent=profit_pct,
            streaks=random.randint(0, 12),
            winRate=win_rate,
            totalTrades=total_trades,
            profitableTrades=profitable_trades,
            avgTradeSize=random.uniform(50, 500),
            maxDrawdown=random.uniform(5, 35),
            crowdDeviation=random.uniform(0, 35),
        )

        settings = AgentSettings(
            maxPositionSize=15 + random.random()*20,
            maxTradesPerDay=5 + random.randint(0, 15),
            autoApprove=random.random() > 0.3,
            safetyExits=[
                SafetyExit(id="1", type="max_daily_loss", threshold=5 + random.random()*15, enabled=True),
                SafetyExit(id="2", type="max_drawdown", threshold=20 + random.random()*20, enabled=True),
                SafetyExit(id="3", type="fraud_alert", threshold=0, enabled=True),
            ],
        )

        portfolio = Portfolio(
            agentId=f"agent_{i+1}",
            usdcBalance=usdc_balance,
            totalValue=total_value,
            positions=positions,
            trades=[],
            lastUpdated=now,
        )

        agent = Agent(
            id=f"agent_{i+1}",
            botId=_rand_bot_id(),
            name=f"Agent {names[i]}" if i < len(names) else f"Agent {i+1}",
            userId=user_id,
            strategy=AgentStrategy(type=random.choice(strategies), copyMode=random.choice([None,"mirror","rules","strategy"])),
            riskness=random.randint(0, 100),
            status="active" if random.random() > 0.1 else ("paused" if random.random() > 0.5 else "exited"),
            portfolio=portfolio,
            settings=settings,
            performance=perf,
            createdAt=now - dt.timedelta(days=random.randint(1, 60)),
            lastTradeAt=now - dt.timedelta(hours=random.randint(1, 72)),
        )
        agents.append(agent)

    return agents

def calculate_crowd_metrics(sample_agents: List[Agent]) -> CrowdMetrics:
    if not sample_agents:
        return CrowdMetrics(avgRiskness=50, avgPositionSize=20, avgWinRate=55, momentumScore=50, strainScore=50, similarityScore=50)

    avg_risk = int(sum(a.riskness for a in sample_agents)/len(sample_agents))
    avg_pos = sum(a.settings.maxPositionSize for a in sample_agents)/len(sample_agents)
    avg_wr = sum(a.performance.winRate for a in sample_agents)/len(sample_agents)

    momentum = min(100.0, max(0.0, 40 + random.random()*40 + (avg_wr-50)*0.3))
    strain = min(100.0, max(0.0, 30 + random.random()*50))
    similarity = min(100.0, max(0.0, 45 + random.random()*35))

    return CrowdMetrics(
        avgRiskness=avg_risk,
        avgPositionSize=avg_pos,
        avgWinRate=avg_wr,
        momentumScore=momentum,
        strainScore=strain,
        similarityScore=similarity,
    )

def generate_leaderboard(agents: List[Agent], size: int = 10) -> List[LeaderboardEntry]:
    entries: List[LeaderboardEntry] = []
    pool = agents[:]
    while len(pool) < size:
        pool.append(random.choice(agents) if agents else generate_mock_agents(1)[0])

    tmp = []
    for a in pool[:size]:
        tmp.append((a.performance.totalProfitPercent + random.uniform(-5, 5), a))
    tmp.sort(key=lambda t: t[0], reverse=True)

    for i, (_, a) in enumerate(tmp, start=1):
        entries.append(LeaderboardEntry(
            rank=i,
            botId=a.botId,
            name=a.name,
            profitPercent=a.performance.totalProfitPercent,
            winRate=a.performance.winRate,
            riskness=a.riskness,
        ))
    return entries
