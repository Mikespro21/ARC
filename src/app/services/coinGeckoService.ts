// CoinGecko API Service for Real Market Data
import { ENV_CONFIG } from '@/app/config/env';
import { MarketData } from '@/app/types';

class CoinGeckoService {
  private baseUrl = ENV_CONFIG.COINGECKO_API_URL;
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private cacheTimeout = 30000; // 30 seconds

  // Get market data for multiple coins
  async getMarketData(coinIds: string[] = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot']): Promise<MarketData[]> {
    const cacheKey = `markets_${coinIds.join(',')}`;
    const cached = this.getFromCache(cacheKey);
    if (cached) return cached;

    try {
      const ids = coinIds.join(',');
      const response = await fetch(
        `${this.baseUrl}/coins/markets?vs_currency=usd&ids=${ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h`
      );

      if (!response.ok) {
        throw new Error(`CoinGecko API error: ${response.status}`);
      }

      const data = await response.json();
      const marketData: MarketData[] = data.map((coin: any) => ({
        id: coin.id,
        symbol: coin.symbol.toUpperCase(),
        name: coin.name,
        currentPrice: coin.current_price,
        priceChange24h: coin.price_change_24h || 0,
        priceChangePercent24h: coin.price_change_percentage_24h || 0,
        marketCap: coin.market_cap || 0,
        volume24h: coin.total_volume || 0,
        high24h: coin.high_24h || coin.current_price,
        low24h: coin.low_24h || coin.current_price,
        lastUpdated: new Date(),
        image: coin.image,
      }));

      this.setCache(cacheKey, marketData);
      return marketData;
    } catch (error) {
      console.error('Error fetching market data:', error);
      // Return mock data in case of error
      return this.getMockMarketData(coinIds);
    }
  }

  // Get price for a single coin
  async getPrice(coinId: string): Promise<number> {
    const cacheKey = `price_${coinId}`;
    const cached = this.getFromCache(cacheKey);
    if (cached) return cached;

    try {
      const response = await fetch(
        `${this.baseUrl}/simple/price?ids=${coinId}&vs_currencies=usd`
      );

      if (!response.ok) {
        throw new Error(`CoinGecko API error: ${response.status}`);
      }

      const data = await response.json();
      const price = data[coinId]?.usd || 0;
      
      this.setCache(cacheKey, price);
      return price;
    } catch (error) {
      console.error(`Error fetching price for ${coinId}:`, error);
      // Return mock price
      return this.getMockPrice(coinId);
    }
  }

  // Search for coins
  async searchCoins(query: string): Promise<Array<{ id: string; name: string; symbol: string; image?: string }>> {
    try {
      const response = await fetch(`${this.baseUrl}/search?query=${query}`);
      
      if (!response.ok) {
        throw new Error(`CoinGecko API error: ${response.status}`);
      }

      const data = await response.json();
      return data.coins.slice(0, 10).map((coin: any) => ({
        id: coin.id,
        name: coin.name,
        symbol: coin.symbol.toUpperCase(),
        image: coin.large || coin.thumb,
      }));
    } catch (error) {
      console.error('Error searching coins:', error);
      return [];
    }
  }

  // Get trending coins
  async getTrendingCoins(): Promise<MarketData[]> {
    const cacheKey = 'trending';
    const cached = this.getFromCache(cacheKey);
    if (cached) return cached;

    try {
      const response = await fetch(`${this.baseUrl}/search/trending`);
      
      if (!response.ok) {
        throw new Error(`CoinGecko API error: ${response.status}`);
      }

      const data = await response.json();
      const coinIds = data.coins.slice(0, 7).map((item: any) => item.item.id);
      
      const marketData = await this.getMarketData(coinIds);
      this.setCache(cacheKey, marketData);
      return marketData;
    } catch (error) {
      console.error('Error fetching trending coins:', error);
      return this.getMockMarketData(['bitcoin', 'ethereum', 'solana']);
    }
  }

  // Cache helpers
  private getFromCache(key: string): any {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }
    return null;
  }

  private setCache(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  // Mock data for demo/fallback
  private getMockMarketData(coinIds: string[]): MarketData[] {
    const mockPrices: Record<string, number> = {
      bitcoin: 45000,
      ethereum: 2500,
      solana: 100,
      cardano: 0.5,
      polkadot: 7,
      binancecoin: 350,
      ripple: 0.6,
      dogecoin: 0.08,
    };

    return coinIds.map(id => ({
      id,
      symbol: id.substring(0, 3).toUpperCase(),
      name: id.charAt(0).toUpperCase() + id.slice(1),
      currentPrice: mockPrices[id] || 1,
      priceChange24h: (Math.random() - 0.5) * 100,
      priceChangePercent24h: (Math.random() - 0.5) * 10,
      marketCap: (mockPrices[id] || 1) * 1000000000,
      volume24h: (mockPrices[id] || 1) * 100000000,
      high24h: (mockPrices[id] || 1) * 1.05,
      low24h: (mockPrices[id] || 1) * 0.95,
      lastUpdated: new Date(),
    }));
  }

  private getMockPrice(coinId: string): number {
    const mockPrices: Record<string, number> = {
      bitcoin: 45000,
      ethereum: 2500,
      solana: 100,
      cardano: 0.5,
      polkadot: 7,
    };
    return mockPrices[coinId] || 1;
  }
}

export const coinGeckoService = new CoinGeckoService();
