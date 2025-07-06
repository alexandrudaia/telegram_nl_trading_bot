import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError, UsernameNotOccupiedError, ChannelInvalidError
import pandas as pd
from collections import defaultdict
import logging
from datetime import datetime, timedelta, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramScraper:
    def __init__(self, api_id: str, api_hash: str, phone: str, channels: list):
        """Initialize the scraper with Telegram credentials and channels"""
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.channels = channels
        self.client = None
        self.messages = defaultdict(lambda: defaultdict(list))  # Store messages by hour and channel

    async def connect(self):
        """Establish connection to Telegram"""
        try:
            self.client = TelegramClient('telegram_scraper_session', self.api_id, self.api_hash)
            await self.client.start()
            
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone)
                code = input('Enter the code received: ')
                await self.client.sign_in(self.phone, code)
            
            logger.info("Successfully connected to Telegram")
            return True
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    async def fetch_messages(self, hours: int = 10000):  # Updated to fetch messages for 1000 hours
        """Fetch messages from the specified channels"""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        
        for channel_url in self.channels:
            try:
                logger.info(f"Fetching messages from {channel_url}")
                channel = await self.client.get_entity(channel_url)
                
                async for message in self.client.iter_messages(channel):
                    if message.date < start_time:
                        break  # Stop fetching messages older than the start time
                    
                    if message and message.text:  # Only process messages with text
                        hour_key = message.date.strftime('%Y-%m-%d %H:00:00')
                        self.messages[hour_key][channel_url.split('/')[-1]].append(message.text.strip())
                        
                    await asyncio.sleep(0.5)  # Rate limiting
                    
            except (UsernameNotOccupiedError, ChannelInvalidError) as e:
                logger.error(f"Invalid channel {channel_url}: {str(e)}")
            except Exception as e:
                logger.error(f"Error fetching from {channel_url}: {str(e)}")

    def aggregate_messages(self):
        """Aggregate messages by hour with channel information"""
        aggregated_data = []
        
        # Generate all hour keys for the last 1000 hours
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=10000)
        current_time = start_time.replace(minute=0, second=0, microsecond=0)
        
        while current_time <= end_time:
            hour_key = current_time.strftime('%Y-%m-%d %H:00:00')
            messages_this_hour = self.messages.get(hour_key, {})
            
            combined_texts = []
            for channel, texts in messages_this_hour.items():
                if texts:
                    combined_texts.append(f"[{channel}]: " + " | ".join(texts))
            
            if combined_texts:
                aggregated_data.append({
                    'hour': hour_key,
                    'text': '\n'.join(combined_texts)
                })
            else:
                aggregated_data.append({
                    'hour': hour_key,
                    'text': 'No messages'
                })
            
            current_time += timedelta(hours=1)
        
        return aggregated_data

    def save_to_csv(self, filename: str = 'telegram_data.csv'):
        """Save aggregated messages to CSV"""
        try:
            aggregated_data = self.aggregate_messages()
            df = pd.DataFrame(aggregated_data)
            df['hour'] = pd.to_datetime(df['hour'])
            df = df.sort_values('hour')
            df.to_csv(filename, index=False)
            logger.info(f"Saved {len(aggregated_data)} hours of data to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")

    async def run_real_time(self):
        """Run the scraper in real-time, continuously fetching new data"""
        while True:
            try:
                logger.info("Starting new real-time scraping cycle...")
                await self.fetch_messages(hours=1)  # Fetch data for the last hour
                
                # Save new data to the CSV
                self.save_to_csv('real_time_telegram_data.csv')
                
                logger.info("Sleeping for 1 hour before the next cycle...")
                await asyncio.sleep(3600)  # Sleep for 1 hour
            except Exception as e:
                logger.error(f"Error in real-time scraping: {str(e)}")
                await asyncio.sleep(60)  # Sleep for 1 minute before retrying

async def main():
    # List of Telegram channels to scrape
    channels = [
    # Major Cryptocurrency Exchanges (Official)
    "binance_announcements",    # Binance Official
    "binance_trading",         # Binance Trading
    "binance_futures",         # Binance Futures
    "cryptocom_official",      # Crypto.com Official
    "kucoin_exchange",        # KuCoin Exchange
    "kraken_exchange",        # Kraken Exchange
    "ftx_official",           # FTX Official
    "huobi_global",           # Huobi Global
    "okx_english",            # OKX Exchange
    "gate_io",               # Gate.io Exchange
    
    # Major News Outlets
    "Cointelegraph",          # Cointelegraph
    "CoinDesk",              # CoinDesk
    "BitcoinMagazine",       # Bitcoin Magazine
    "DecryptMedia",          # Decrypt
    "TheBlock",              # The Block
    "cryptoslate",           # CryptoSlate
    "BeInCrypto",            # BeInCrypto
    "CryptoNews",            # CryptoNews
    "coinrivet",             # CoinRivet
    "ambcrypto",             # AMBCrypto
    
    # Market Analysis & Data
    "WhaleAlert",            # Whale Alert
    "glassnode",            # Glassnode Alerts
    "santimentfeed",        # Santiment
    "cryptoquant",          # CryptoQuant
    "messaricrypto",        # Messari
    "IntoTheBlock",         # IntoTheBlock
    "CoinGeckoOfficial",    # CoinGecko
    "CMCAlerts",            # CoinMarketCap Alerts
    "DeFiLlama",            # DeFi Llama
    "TokenTerminal",        # Token Terminal
    
    # Major DeFi Protocols
    "uniswap",              # Uniswap
    "AaveAave",             # Aave
    "CurveFinance",         # Curve Finance
    "SushiSwap_org",        # SushiSwap
    "PancakeSwap",          # PancakeSwap
    "Compound",             # Compound
    "MakerDAO",             # MakerDAO
    "chainlink",            # Chainlink
    "1inch",                # 1inch Exchange
    "yearnfinance",         # Yearn Finance
    
    # Top Crypto Influencers
    "CryptoBanter",         # Crypto Banter
    "MMCrypto",             # MMCrypto
    "CryptoCapital",        # Crypto Capital Venture
    "TheMoonCarl",          # The Moon
    "cryptomichael",        # Crypto Michael
    "CryptoWendyO",         # Wendy O
    "scottmelker",          # The Wolf Of All Streets
    "RaoulGMI",             # Raoul Pal
    "SheldonEvans",         # Sheldon Evans
    "BitBoy_Crypto",        # BitBoy Crypto

    # Research & Analysis
    "InvestAnswers",        # Invest Answers
    "RealVision",           # Real Vision
    "TokenMetrics",         # Token Metrics
    "MessariCrypto",        # Messari Crypto
    "DappRadar",            # DappRadar
    "nansen_ai",            # Nansen AI
    "defiant_main",         # The Defiant
    "tokenterminal",        # Token Terminal
    "DefiPrime",            # DeFi Prime
    "DefiPulse",            # DeFi Pulse

    # Trading Signals & Analysis
    "CryptoSignals",        # Crypto Signals
    "CryptoTradingRoom",    # Crypto Trading Room
    "AltSignals",           # Alt Signals
    "CryptoVIPSignal",      # Crypto VIP Signal
    "BinanceFuturesSignals", # Binance Futures Signals
    "CryptoTrading_Signals", # Crypto Trading Signals
    "CryptoAlerts",         # Crypto Alerts
    "TradingCrypto",        # Trading Crypto
    "CryptoTraders",        # Crypto Traders
    "TradingView_Signals"   # TradingView Signals
]


    scraper = TelegramScraper(
 
        phone="+",
        channels=channels
    )

    if await scraper.connect():
        # Fetch historical data for 1000 hours
        await scraper.fetch_messages(hours=10000)
        scraper.save_to_csv('historical_telegram_data.csv')
        
        logger.info("Sleeping for 1 hour before starting real-time scraping...")
        await asyncio.sleep(3600)  # Sleep for 1 hour before starting real-time scraping
        
        # Start real-time scraping
        await scraper.run_real_time()

if __name__ == "__main__":
    asyncio.run(main())
