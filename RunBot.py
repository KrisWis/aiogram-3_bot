from InstanceBot import bot, dp
import database
import asyncio
import handlers

async def main() -> None:

    database.db.check_db()

    handlers.hand_user.hand_add()

    bot_name = await bot.get_me()

    print(f'Бот запущен - {bot_name.first_name}')

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())