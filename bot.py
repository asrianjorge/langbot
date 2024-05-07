import asyncio
from aiogram import Bot, Dispatcher
from aiogram.methods import SetMyDescription

from handlers import user_commands
from callbacks import packs, subscription, train, main_commands
from modules import support_module, payment_module, premium_module, settings_module

from config_reader import config
from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import AntiFloodMiddleware
from modules.payment_module import process_pre_checkout_query
from utils.database import db_start, db_settings_start


# logic
# тренировки:
# 1) учить слова
# 2) смотреть видосы, интервью
# 3) слушать песни и учить слова
# 4) пройти тест чтобы узнать свой уровень *
# 5) выучить акценты (британский/американский) *


async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    # dp.message.middleware(CheckSubscription())
    dp.message.middleware(AntiFloodMiddleware())

    dp.pre_checkout_query.register(process_pre_checkout_query)
    # dp.message.register(successful_payment, SuccessfulPayment)

    dp.include_routers(
        subscription.router,
        user_commands.router,
        main_commands.router,
        support_module.router,
        train.router,
        payment_module.router,
        settings_module.router,
        premium_module.router,
        packs.router,
    )

    await bot(SetMyDescription(
        description="hello! it is a bot created for improving your english 🇬🇧 and spanish 🇪🇸 skills"))
    await bot.delete_webhook(drop_pending_updates=True)
    await db_start()
    await db_settings_start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
