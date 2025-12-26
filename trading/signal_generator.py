import os
import asyncio
from datetime import datetime
from trading.pocket_client import PocketOptionClient
from trading.analyzer import MarketAnalyzer
from bot.telegram_bot import send_signal
import logging

class SignalGenerator:
    """Генератор сигналів з фільтрацією >70%"""
    
    def __init__(self):
        self.pocket_client = PocketOptionClient()
        self.analyzer = MarketAnalyzer()
        self.min_confidence = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", 0.70))
        
    async def check_and_generate_signals(self):
        """Головна функція генерації сигналів"""
        await self.pocket_client.connect()
        
        # Список активів для моніторингу
        assets_to_monitor = [
            ("GBPJPY_otc", 120),  # 2 хвилини
            # Додайте інші пари тут
        ]
        
        for asset, timeframe in assets_to_monitor:
            try:
                # 1. Отримуємо дані
                candles = await self.pocket_client.get_candles(
                    asset=asset, 
                    timeframe=timeframe, 
                    count=100
                )
                
                if candles.empty:
                    continue
                    
                # 2. Аналізуємо через AI
                signal = await self.analyzer.analyze_market(
                    asset=asset,
                    timeframe_seconds=timeframe,
                    candles_data=candles
                )
                
                # 3. Фільтруємо (>70%)
                if signal and signal.get('confidence', 0) >= self.min_confidence:
                    # Формуємо повідомлення
                    message = self._format_signal_message(
                        asset=asset,
                        timeframe=timeframe,
                        signal=signal,
                        current_price=await self.pocket_client.get_current_price(asset)
                    )
                    
                    # 4. Надсилаємо в Telegram
                    await send_signal(message)
                    logging.info(f"Надіслано сигнал: {asset}")
                    
            except Exception as e:
                logging.error(f"Помилка для {asset}: {e}")
                
        await self.pocket_client.disconnect()
    
    def _format_signal_message(self, asset: str, timeframe: int, signal: dict, current_price: float) -> str:
        """Форматує сигнал у зручний для читання вигляд"""
        timeframe_min = timeframe // 60
        
        return f"""
🚨 **ТОРГОВИЙ СИГНАЛ** 🚨

📊 **Актив:** {asset}
⏰ **Таймфрейм:** {timeframe_min} хвилин
🎯 **Напрямок:** {signal['direction']}
📈 **Вірогідність:** {signal['confidence']*100:.1f}%
💵 **Поточна ціна:** {current_price if current_price else 'N/A'}
🕒 **Час сигналу:** {datetime.now().strftime('%H:%M:%S')}
📝 **Причина:** {signal['reason']}

#сигнал #{asset.replace('/', '').replace('_otc', '')}
        """.strip()
