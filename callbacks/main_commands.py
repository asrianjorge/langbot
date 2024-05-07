from datetime import date
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from handlers.user_commands import main_menu
from keyboards import inline, builders
from utils.database import db_settings_get_data, db_check_pro, db_settings_get_theme
from utils.states import Settings

router = Router()


@router.callback_query(inline.UserCommand.filter(F.action == "train"))
async def training_mode(call: CallbackQuery, callback_data: inline.Language):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    image = FSInputFile(f"./data/{theme}/choose_training.png")
    input_image = InputMediaPhoto(media=image)

    li = await db_check_pro(call.from_user.id)
    if li[0]:
        await call.message.edit_media(
            media=input_image,
            inline_message_id=call.inline_message_id,
            reply_markup=builders.train_pro_kb()
        )
    else:
        await call.message.edit_media(
            media=input_image,
            inline_message_id=call.inline_message_id,
            reply_markup=builders.train_kb()
        )


@router.callback_query(inline.UserCommand.filter(F.action == "about"))
async def about(call: CallbackQuery, state: FSMContext):
    # await state.set_state(Settings.theme)
    # t = await state.get_data()
    # tt = list(t.values())
    # print('settings:', tt[0])
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    image = FSInputFile(f"./data/{theme}/about.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=inline.about_kb_1
    )


@router.callback_query(inline.UserCommand.filter(F.action == "roadmap"))
async def about(call: CallbackQuery, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    image = FSInputFile(f"./data/{theme}/roadmap.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        reply_markup=inline.about_kb_2
    )


@router.callback_query(inline.UserCommand.filter(F.action == "sub_info"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    await call.message.delete()
    # set_data = await db_settings_get_data(call.from_user.id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)
    image = FSInputFile(f'./data/{theme}/subscription.png')

    check = await db_check_pro(call.from_user.id)
    flag, exp_date = check[0], check[1]
    
    if flag:
        # image = FSInputFile(f"./data/{theme}/roadmap.png")
        # input_image = InputMediaPhoto(media=image)
        print(exp_date)
        print(date.fromisoformat(exp_date[0]))
        d = date.fromisoformat(exp_date[0]).strftime("%d of %B %Y, %A")
        if d[0] == '0':
            d = d[1:]
        await call.message.answer_photo(
            photo=image,
            text=f'your premium subscription will expire on the {d}',
            reply_markup=inline.expand_or_stop_premium
        )
        
    else:
        await call.message.answer_photo(
            photo=image,
            text=f"you haven't an active premium subscription now. do you want to get it?",
            reply_markup=inline.expand_or_stop_premium
        )
        


@router.callback_query(inline.UserCommand.filter(F.action == "achievements"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    pass


@router.callback_query(inline.UserCommand.filter(F.action == "profile"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    pass


@router.callback_query(inline.UserCommand.filter(F.action == "donate"))
async def packs_handler(call: CallbackQuery, callback_data: inline.UserCommand):
    pass


@router.callback_query(inline.UserCommand.filter(F.action == "premium"))
async def packs_handler(call: CallbackQuery, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    image = FSInputFile(f"./data/{theme}/pro_level1.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=inline.premium_kb
    )
    
    
@router.callback_query(inline.UserCommand.filter(F.action == "premium2"))
async def packs_handler(call: CallbackQuery, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    image = FSInputFile(f"./data/{theme}/pro_level2.png")
    input_image = InputMediaPhoto(media=image)
    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=inline.premium_kb_2
    )


# @router.callback_query(builders.UserCommand.filter(F.action == "to_main_menu"))
# async def packs_handler(call: CallbackQuery, state: FSMContext):
#     # image = FSInputFile("./data/main_menu.png")
#     await call.message.delete_reply_markup()
#     await main_menu(call.message, state)
#     # await call.message.answer_photo(
#     #     image,
#     #     reply_markup=inline.main_menu
#     # )
#
#
# @router.callback_query(inline.UserCommand.filter(F.action == "main_menu"))
# async def packs_handler(call: CallbackQuery, state: FSMContext):
#     await main_menu(call.message, state)
#     # await state.set_state(Settings.theme)
#     # t = await state.get_data()
#     # tt = list(t.values())
#     # print('settings:', tt[0])
#     # theme = tt[0]
#     #
#     # image = FSInputFile(f"./data/{theme}/main_menu.png")
#     # input_image = InputMediaPhoto(media=image)
#     # await call.message.edit_media(
#     #     input_image,
#     #     reply_markup=inline.main_menu
#     # )
#
#
# @router.callback_query(builders.UserCommand.filter(F.action == "main_menu"))
# async def packs_handler(call: CallbackQuery, state: FSMContext):
#     await main_menu(call.message, state)
#
#     # image = FSInputFile("./data/main_menu.png")
#     # input_image = InputMediaPhoto(media=image)
#     # await call.message.edit_media(
#     #     input_image,
#     #     reply_markup=inline.main_menu
#     # )
