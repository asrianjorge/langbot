from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, InputMediaPhoto, \
    Message
from aiogram.fsm.state import StatesGroup, State

from keyboards import inline, builders
from keyboards.inline import UserCommand
from utils.database import db_settings_get_theme, db_settings_update_theme, db_settings_get_data
from utils.states import Settings

router = Router()


@router.callback_query(UserCommand.filter(F.action == 'settings'))
async def settings_handler(call: CallbackQuery, state: FSMContext):
    # await state.set_state(Settings.theme)
    # t = await state.get_data()
    # tt = list(t.values())
    # print(tt)
    # print('settings:', tt[0])
    # theme = tt[0]
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    image = FSInputFile(f"./data/{theme}/settings.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image,
        reply_markup=inline.settings_kb_pro
    )


@router.callback_query(UserCommand.filter(F.action == 'themes'))
async def themes_handler(call: CallbackQuery, state: FSMContext):
    # await state.set_state(Settings.theme)
    # t = await state.get_data()
    # tt = list(t.values())
    # print('settings:', tt[0])
    # theme = tt[0]
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    image = FSInputFile(f"./data/{theme}.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image,
        reply_markup=inline.themes_kb
    )


@router.callback_query(UserCommand.filter(F.action == 'color_flash_theme'))
async def themes_handler(call: CallbackQuery, state: FSMContext):
    # await state.set_state(Settings.theme)
    # await state.update_data(theme='color_flash_theme')
    # t = await state.get_data()
    # tt = list(t.values())
    # print('settings:', tt[0])
    # theme = tt[0]

    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]

    theme = 'color_flash_theme'

    print(call.message.from_user.id)
    await db_settings_update_theme(call.from_user.id, theme)

    image = FSInputFile(f"./data/{theme}.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image,
        reply_markup=inline.themes_kb
    )


@router.callback_query(UserCommand.filter(F.action == 'basic_theme'))
async def themes_handler(call: CallbackQuery, state: FSMContext):
    theme = 'basic_theme'

    print(call.message.from_user.id)
    await db_settings_update_theme(call.from_user.id, theme)

    image = FSInputFile(f"./data/{theme}.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image,
        reply_markup=inline.themes_kb
    )


@router.callback_query(UserCommand.filter(F.action == 'white_diamond_theme'))
async def themes_handler(call: CallbackQuery, state: FSMContext):
    theme = 'white_diamond_theme'

    await db_settings_update_theme(call.from_user.id, theme)

    image = FSInputFile(f"./data/{theme}.png")
    input_image = InputMediaPhoto(media=image)

    await call.message.edit_media(
        input_image,
        reply_markup=inline.themes_kb
    )
