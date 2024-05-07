from time import sleep

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto

from handlers.user_commands import start
from keyboards import inline
from utils.database import db_settings_get_theme, db_update_pro, db_settings_get_data

router = Router()


async def apply_premium(message: Message):
    sleep(1)
    await message.answer(
        text='now the new main menu will appear'
    )
    sleep(1)
    await message.answer(
        text='3'
    )
    sleep(1)
    await message.answer(
        text='2'
    )
    sleep(1)
    await message.answer(
        text='1'
    )
    sleep(1)
    await message.answer(
        text='are you ready for a miracle?'
    )
    sleep(1)
    await start(message)


@router.callback_query(inline.UserCommand.filter(F.action == "pro_features"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)
    image = FSInputFile(f"./data/{theme}/pro_features.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=inline.premium_kb1
    )


@router.callback_query(inline.UserCommand.filter(F.action == "how_it_works"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)
    image = FSInputFile(f"./data/{theme}/how_it_works.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=inline.premium_kb2
    )
