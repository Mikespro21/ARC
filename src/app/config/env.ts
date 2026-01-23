// Environment Configuration for Crowdlike
// These can be set via environment variables in production

export const ENV_CONFIG = {
  // CoinGecko API (no key required for demo endpoints)
  COINGECKO_API_URL: import.meta.env.VITE_COINGECKO_API_URL || 'https://api.coingecko.com/api/v3',
  COINGECKO_API_KEY: import.meta.env.VITE_COINGECKO_API_KEY || '', // Optional for rate limits
  
  // Blockchain Configuration
  ARC_RPC_URL: import.meta.env.VITE_ARC_RPC_URL || 'https://arc-testnet.rpc.url',
  ARC_CHAIN_ID: import.meta.env.VITE_ARC_CHAIN_ID || '1',
  
  QUBIC_RPC_URL: import.meta.env.VITE_QUBIC_RPC_URL || 'https://qubic-testnet.rpc.url',
  QUBIC_CHAIN_ID: import.meta.env.VITE_QUBIC_CHAIN_ID || '1',
  
  // Circle USDC Configuration
  CIRCLE_API_KEY: import.meta.env.VITE_CIRCLE_API_KEY || '',
  CIRCLE_API_URL: import.meta.env.VITE_CIRCLE_API_URL || 'https://api-sandbox.circle.com',
  USDC_CONTRACT_ADDRESS: import.meta.env.VITE_USDC_CONTRACT_ADDRESS || '0x...',
  
  // Wallet Configuration
  DEFAULT_WALLET_PROVIDER: import.meta.env.VITE_WALLET_PROVIDER || 'metamask',
  TESTNET_MODE: import.meta.env.VITE_TESTNET_MODE !== 'false', // Default to testnet
  
  // App Configuration
  APP_VERSION: '1.7.0',
  ENABLE_DEMO_MODE: import.meta.env.VITE_DEMO_MODE !== 'false', // Demo mode with mock data
  MARKET_DATA_REFRESH_INTERVAL: parseInt(import.meta.env.VITE_MARKET_REFRESH_INTERVAL || '30000'), // 30s
  PORTFOLIO_REFRESH_INTERVAL: parseInt(import.meta.env.VITE_PORTFOLIO_REFRESH_INTERVAL || '5000'), // 5s
  
  // Agent Configuration
  MAX_AGENTS_PER_USER: parseInt(import.meta.env.VITE_MAX_AGENTS || '10'),
  MIN_AGENT_BALANCE: parseFloat(import.meta.env.VITE_MIN_AGENT_BALANCE || '100'), // Min USDC
  
  // Trading Configuration
  ENABLE_PAPER_TRADING: import.meta.env.VITE_PAPER_TRADING !== 'false',
  TRADING_FEES: parseFloat(import.meta.env.VITE_TRADING_FEES || '0'), // 0% for demo
  SLIPPAGE: parseFloat(import.meta.env.VITE_SLIPPAGE || '0'), // 0% for demo
};

// Helper to check if running in demo mode
export const isDemoMode = () => ENV_CONFIG.ENABLE_DEMO_MODE;

// Helper to get full API URLs
export const getApiUrl = (service: 'coingecko' | 'arc' | 'qubic' | 'circle') => {
  switch (service) {
    case 'coingecko':
      return ENV_CONFIG.COINGECKO_API_URL;
    case 'arc':
      return ENV_CONFIG.ARC_RPC_URL;
    case 'qubic':
      return ENV_CONFIG.QUBIC_RPC_URL;
    case 'circle':
      return ENV_CONFIG.CIRCLE_API_URL;
    default:
      return '';
  }
};

// Configuration display for Settings/Profile page
export const getEnvConfigForDisplay = () => ({
  'App Version': ENV_CONFIG.APP_VERSION,
  'Demo Mode': ENV_CONFIG.ENABLE_DEMO_MODE ? 'Enabled' : 'Disabled',
  'Testnet Mode': ENV_CONFIG.TESTNET_MODE ? 'Enabled' : 'Disabled',
  'Paper Trading': ENV_CONFIG.ENABLE_PAPER_TRADING ? 'Enabled' : 'Disabled',
  'CoinGecko API': ENV_CONFIG.COINGECKO_API_URL,
  'Arc RPC': ENV_CONFIG.ARC_RPC_URL,
  'Qubic RPC': ENV_CONFIG.QUBIC_RPC_URL,
  'Circle API': ENV_CONFIG.CIRCLE_API_URL,
  'USDC Contract': ENV_CONFIG.USDC_CONTRACT_ADDRESS,
  'Max Agents': ENV_CONFIG.MAX_AGENTS_PER_USER,
  'Market Refresh': `${ENV_CONFIG.MARKET_DATA_REFRESH_INTERVAL / 1000}s`,
});
