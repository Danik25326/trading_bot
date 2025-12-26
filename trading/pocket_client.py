import os
import aiohttp
import pandas as pd
from typing import Optional, List
import logging

class PocketOptionClient:
    """Оновлений клієнт для Pocket Option API з OAuth2 токеном"""
    
    def __init__(self):
        self.ssid = os.getenv("POCKET_OPTION_SSID")
        self.base_url = "https://api-pocketoption.com"  # або demo-версія
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "Authorization": f"Bearer {self.ssid}",
            "Content-Type": "application/json"
        }
        
    async def connect(self):
        """Створює сесію (не потрібно WebSocket для даних)"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        logging.info("PocketOption клієнт ініціалізовано з OAuth2 токеном")
        
    async def get_candles(self, asset: str, timeframe: int, count: int = 100) -> pd.DataFrame:
        """
        Отримує історичні дані через REST API
        
        Приклад asset: 'GBPJPY_otc'
        Приклад timeframe: 120 (секунд)
        """
        if not self.session:
            await self.connect()
            
        try:
            # Ендпоінт може відрізнятися - перевірте документацію API
            url = f"{self.base_url}/api/v2/chart/history"
            params = {
                "symbol": asset,
                "timeframe": timeframe,
                "count": count
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # Конвертуємо у DataFrame
                    df = pd.DataFrame(data['candles'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                    df.set_index('timestamp', inplace=True)
                    return df
                else:
                    logging.error(f"Помилка отримання даних: {response.status}")
                    return pd.DataFrame()
                    
        except Exception as e:
            logging.error(f"Помилка: {e}")
            return pd.DataFrame()
            
    async def get_current_price(self, asset: str) -> Optional[float]:
        """Отримує поточну ціну активу"""
        # Швидкий запит для отримання поточної ціни
        url = f"{self.base_url}/api/v2/quote"
        params = {"symbols": asset}
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data[asset]['price']
        return None
        
    async def disconnect(self):
        """Закриває сесію"""
        if self.session:
            await self.session.close()
