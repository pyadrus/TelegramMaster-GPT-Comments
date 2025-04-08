# -*- coding: utf-8 -*-
from groq import AsyncGroq
from loguru import logger

from src.config import GROQ_API_KEY, selectedmodel
from src.proxy_config import setup_proxy


async def get_groq_response(user_input):
    """Получение ответа от Groq API."""
    setup_proxy()  # Установка прокси
    # Инициализация Groq клиента
    client_groq = AsyncGroq(api_key=GROQ_API_KEY)
    try:
        # Формируем запрос к Groq API
        chat_completion = await client_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Ты патриот России, дай хороший ответ на этот пост: {user_input}",
                }
            ],
            model=f"{selectedmodel}",
        )
        # Возвращаем ответ от ИИ
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.exception(e)
