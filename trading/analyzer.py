import os
import groq
import pandas as pd
from typing import Optional, Dict

class MarketAnalyzer:
    """Аналізує ринкові дані за допомогою GROQ LLaMA AI."""
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

    def prepare_ai_prompt(self, df: pd.DataFrame, asset: str, timeframe: str) -> str:
        """
        Готує технічне завдання для AI на основі даних графіка.
        Тут потрібно ваш налаштований промпт, який навчає AI аналізувати графіки.
        """
        # Приклад простого промпта. Вам потрібно його детально продумати!
        prompt = f"""
        Ти — експертний трейдер. Проаналізуй такі ринкові дані для {asset} на {timeframe} хвилинному графіку:
        Останні 10 значень закриття: {df['close'].tail(10).tolist()}.
        Поточна ціна: {df['close'].iloc[-1]}.
        Відносна мінливість: {df['close'].pct_change().std():.5f}.

        Надай аналіз у такому строгому форматі JSON:
        {{
            "direction": "UP" or "DOWN",
            "confidence": число від 0.00 до 1.00,
            "reason": "коротке пояснення"
        }}
        """
        return prompt

    async def analyze_market(self, asset: str, timeframe_seconds: int, candles_data: pd.DataFrame) -> Optional[Dict]:
        """
        Надсилає запит до AI і повертає розпізнаний сигнал.
        """
        timeframe_str = f"{timeframe_seconds // 60} хв"
        prompt = self.prepare_ai_prompt(candles_data, asset, timeframe_str)

        try:
            chat_completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Модель, яку ви вказали
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2, # Для більш консервативних прогнозів
            )
            # Тут потрібно обробити відповідь AI та конвертувати її з JSON
            # Це спрощений приклад, на практиці потрібна перевірка помилок
            analysis_text = chat_completion.choices[0].message.content
            # ... код для парсингу JSON з analysis_text ...
            # parsed_signal = json.loads(analysis_text)

            # Заглушка для прикладу:
            parsed_signal = {"direction": "DOWN", "confidence": 0.75, "reason": "Тестовий сигнал"}
            return parsed_signal

        except Exception as e:
            print(f"Помилка аналізу через AI: {e}")
            return None
