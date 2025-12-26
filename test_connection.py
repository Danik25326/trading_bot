import asyncio
import os
from dotenv import load_dotenv
from trading.pocket_client import PocketOptionClient

load_dotenv()

async def test():
    client = PocketOptionClient()
    await client.connect()
    
    # Тест отримання даних
    df = await client.get_candles("GBPJPY_otc", 120, 10)
    print(f"Отримано {len(df)} свічок")
    print(df.tail())
    
    # Тест поточної ціни
    price = await client.get_current_price("GBPJPY_otc")
    print(f"Поточна ціна: {price}")
    
    await client.disconnect()

asyncio.run(test())
