import asyncio
import logging
import dotenv
import os

from aiogram import Bot, Dispatcher


from app.handlers.user import router as user_router
from app.handlers.admin import router as admin_router

from app.databases.models import redisClient as client


dotenv.load_dotenv()


async def first_load():
    if not await client.connection.exists('group:1'):
        await client.connection.lpush('group:1', *['ban', 'kick'])


async def main():
    await client.connect()

    await first_load()

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_routers(admin_router, user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        client.disconnect()
        print('Бот отключен')
