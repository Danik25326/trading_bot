import os
from pocketoptionapi_async import AsyncPocketOptionClient, TimeFrame
import pandas as pd

class PocketOptionClient:
    """Клієнт для отримання даних з Pocket Option."""
    def __init__(self):
        ssid = os.getenv("POCKET_OPTION_SSID")
        # Використовуйте is_demo=False для реального рахунку
        self.client = AsyncPocketOptionClient(ssid, is_demo=True)

    async def connect(self):
        """Встановлює з'єднання з платформою."""
        await self.client.connect()
        print("Підключено до Pocket Option API")

    async def get_candles_data(self, asset: str, timeframe_seconds: int, count: int = 100):
        """
        Отримує останні свічки для аналізу.
        Аргументи:
          asset: Код активу, наприклад 'GBPJPY_otc'
          timeframe_seconds: Таймфрейм у секундах (наприклад, 120 для 2 хв)
          count: Кількість свічок для отримання
        """
        # Використовуємо метод з бібліотеки, який повертає DataFrame
        df = await self.client.get_candles_dataframe(
            asset=asset,
            timeframe=timeframe_seconds,
            count=count
        )
        return df

    async def disconnect(self):
        """Коректно розриває з'єднання."""
        await self.client.disconnect()
