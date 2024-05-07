from datetime import datetime, timezone
from time import sleep

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, InputMediaPhoto, \
    Message
from aiogram.fsm.state import StatesGroup, State
import openpyxl

from keyboards import inline, builders
from keyboards.inline import UserCommand
from utils.database import db_settings_get_data, db_settings_get_theme

router = Router()


class SupportStateClass(StatesGroup):
    msg = State()


support_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text="❔ частые вопросы", callback_data='faq'),
        # ],
        [
            InlineKeyboardButton(text="✉️ написать в поддержку", callback_data='msg_to_support'),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(action='main_menu').pack()),
        ]
    ]
)


@router.callback_query(inline.UserCommand.filter(F.action == "support"))
async def support_1(call: CallbackQuery, state: FSMContext):
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    await state.set_state(SupportStateClass.msg)
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/support.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image
    )
    await call.message.edit_caption(
        caption="если у вас есть вопросы или предложения по улучшению бота, то вы можете написать нам. мы с радостью прочитаем ваше письмо и ответим на все интересующие вопросы 🤗",
        reply_markup=support_kb
    )


@router.callback_query(F.data == "msg_to_support")
async def support_1(call: CallbackQuery, state: FSMContext):
    await state.set_state(SupportStateClass.msg)
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/msg_support.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        input_image
    )
    await call.message.edit_caption(
        caption="напишите сообщение, и мы передадим его в поддержку",
    )


@router.message(SupportStateClass.msg)
async def support_1(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    # data = await state.get_data()
    # await bot.send_message(
    #     chat_id=7029170577,
    #     # chat_id='@engplusspansupportbot',
    #     text=f'{message.text}\n\n{message.from_user.id}'
    # )

    wb = openpyxl.load_workbook('/home/topg/langbot/langbot-repo/secret/support.xlsx')
    sheet = wb.active
    sheet.append([message.from_user.id, message.from_user.username, message.text, datetime.now()])
    wb.save('/home/topg/langbot/langbot-repo/secret/support.xlsx')

    await message.answer(
        text='ваше сообщение отправлено в поддержку. вам придет уведомление, когда оно будет обработано',
        reply_markup=builders.to_main_menu('👌 отлично')
    )
    await state.clear()
