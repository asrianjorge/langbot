from time import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery

from keyboards import inline, reply, builders
from utils.database import db_settings_get_theme, db_start, db_does_user_exist, db_new_user, db_check_pro, db_settings_first_set, \
    db_settings_get_data
from utils.states import Settings, Temporal

router = Router()
global flag
flag = False


@router.message(Command("start"))
async def start(message: Message):
    # translator = Translator()
    # namee = message.from_user.first_name
    # name = translator.translate(namee, dest='en').text
    
    # await state.set_state(Settings.theme)
    # await state.set_state(Settings.sys_lang)

    # await state.set_state(Temporal.user_id)
    # user_id = await list(state.get_data().values)
    # if user_id is None:
    #     user_id = message.from_user.id
    user_id = message.from_user.id

    if not await db_does_user_exist(user_id):
        # add new user to database
        await db_new_user(user_id, message.from_user.username, message.from_user.first_name)
        await db_settings_first_set(user_id)

        # get settings data
        # set_data = await db_settings_get_data(user_id)
        # theme = set_data[0]
        theme = await db_settings_get_theme(message.from_user.id)

        # create message
        image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/new_member.png")
        # await state.set_state(Form.is_registered)
        # await state.update_data(is_registered='True')
        await message.answer_photo(
            image,
            caption=f"hello 👋\n\n"\
            # f"hello, {name} 👋\n\n"
                    f"nice to see you here! it is a bot created to help you improve you language skills. main menu will appear in seconds\n\n"\
                    f"live long and prosper 🖖",
            # reply_markup=inline.reg
        )
        sleep(2)
        await main_menu(message)
    else:
        await main_menu(message)
        # # get settings data
        # set_data = await db_settings_get_data(user_id)
        # await state.update_data(theme=set_data[0])
        # await state.update_data(sys_lang=set_data[1])
        # t = await state.get_data()
        # tt = list(t.values())
        # print(t)
        # theme = tt[0]
        #
        # # create photo of message
        # image = FSInputFile(f"./data/{theme}/main_menu.png")
        #
        # # create message
        # f = await db_check_pro(user_id)
        # print(f)
        # if f[0]:
        #     await message.answer_photo(
        #         image,
        #         # caption=f"you are in main menu ⚡️",
        #         reply_markup=inline.main_menu_pro
        #     )
        # else:
        #     await message.answer_photo(
        #         image,
        #         # caption=f"you are in main menu ⚡️",
        #         reply_markup=inline.main_menu
        #     )


@router.message(Command("menu"))
async def main_menu(message: Message):
    # await db_settings_first_set(message.from_user.id)

    user_id = message.from_user.id

    # await state.set_state(Settings.theme)
    # await state.set_state(Settings.sys_lang)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = str(set_data[0])
    theme = await db_settings_get_theme(message.from_user.id)

    # await state.update_data(theme=set_data[0])
    # await state.update_data(sys_lang=set_data[1])
    # t = await state.get_data()
    # tt = list(t.values())
    # print(t)
    # theme = tt[0]

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await message.answer_photo(
            photo=image,
            reply_markup=inline.main_menu_pro
        )
    else:
        await message.answer_photo(
            photo=image,
            reply_markup=inline.main_menu
        )


@router.callback_query(inline.UserCommand.filter(F.action == "main_menu"))
async def main_menu_call_1(call: CallbackQuery):
    # await message.delete_reply_markup()

    # await db_settings_first_set(message.from_user.id)
    user_id = call.from_user.id
    # user_id = call.message.from_user.id

    # await state.set_state(Settings.theme)
    # await state.set_state(Settings.sys_lang)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)

    if f[0]:
        await call.message.edit_media(
            input_image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.edit_media(
            input_image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )


@router.callback_query(builders.UserCommand.filter(F.action == "main_menu"))
async def main_menu_call_2(call: CallbackQuery, state: FSMContext):
    # await message.delete_reply_markup()

    # await db_settings_first_set(message.from_user.id)
    user_id = call.from_user.id
    # user_id = call.message.from_user.id

    # await state.set_state(Settings.theme)
    # await state.set_state(Settings.sys_lang)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await call.message.edit_media(
            input_image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.edit_media(
            input_image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )


@router.callback_query(builders.UserCommand.filter(F.action == "to_main_menu"))
async def main_menu_call_3(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    # await db_settings_first_set(message.from_user.id)
    user_id = call.from_user.id
    print(user_id, "VERSUS", call.message.from_user.id)
    # user_id = call.message.from_user.id

    # await state.set_state(Settings.theme)
    # await state.set_state(Settings.sys_lang)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )


@router.callback_query(inline.UserCommand.filter(F.action == "to_main_menu"))
async def main_menu_call_4(call: CallbackQuery):
    await call.message.delete_reply_markup()

    user_id = call.from_user.id
    print(user_id, "VERSUS", call.message.from_user.id)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )


@router.callback_query(builders.UserCommand.filter(F.action == "to_main_menu_with_del"))
async def main_menu_call_5(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    user_id = call.from_user.id
    print(user_id, "VERSUS", call.message.from_user.id)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )


@router.callback_query(inline.UserCommand.filter(F.action == "to_main_menu_with_del"))
async def main_menu_call_6(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    user_id = call.from_user.id
    print(user_id, "VERSUS", call.message.from_user.id)

    # get settings data
    # set_data = await db_settings_get_data(user_id)
    # theme = set_data[0]
    theme = await db_settings_get_theme(call.from_user.id)

    # create photo of message
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    input_image = InputMediaPhoto(media=image)

    # create message
    f = await db_check_pro(user_id)
    print(f)
    if f[0]:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu_pro
        )
    else:
        await call.message.answer_photo(
            image,
            # caption=f"you are in main menu ⚡️",
            reply_markup=inline.main_menu
        )