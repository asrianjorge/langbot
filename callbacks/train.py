import os
from time import sleep

import aiogram
import pandas as pd
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from handlers.user_commands import main_menu
from keyboards import inline, builders
from modules.requests_module import cambridge_dict_find_word
from modules.table_module import delete_from_cambridge_dict, save_to_cambridge_dict, cambridge_dict_first_set, cambridge_dict_iterator
from utils.database import db_settings_get_camb_w_num, db_settings_get_data, db_check_pro, db_does_dict_exists, db_settings_update_camb_w_num, db_update_dict
from utils.states import Dictionary

router = Router()
global calls
global dfr


class Path(StatesGroup):
    path = State()
    sheet = State()


# после выбора тренировки можно выбрать язык:
# встроенные или пользовательские
@router.callback_query(builders.TrainThroughLang.filter(F.next_action == "choose_lang"))
async def train(call: CallbackQuery, callback_data: builders.TrainThroughLang, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    training = callback_data.train

    if training == 'fill_blank' or training == 'match':
        flag = False
    else:
        flag = os.path.exists(f'./data/userdata/dict_{call.from_user.id}.xlsx')

    image = FSInputFile(f"./data/{theme}/choose_lang.png")
    input_image = InputMediaPhoto(media=image)

    await call.message.edit_media(
        media=input_image,
        # caption=f"choose a language to start training",
        reply_markup=builders.eng_or_my_lang(
            training, flag)
    )


# если язык был выбрать пользовательский (my_lang), то сначала надо выбрать, какой именно
# а если встроенный (english_base), то сразу переходим к след. фичам
# так как не обрабатываем этот случай отдельно
@router.callback_query(builders.ActionLang.filter(F.lang == 'my_lang'))
async def train(call: CallbackQuery, callback_data: builders.ActionLang, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    training = callback_data.action

    image = FSInputFile(f"./data/{theme}/choose_lang.png")
    input_image = InputMediaPhoto(media=image)

    # через state бкдем подгружать путь до словаря
    path = f'./data/userdata/dict_{call.from_user.id}.xlsx'
    await state.set_state(Path.path)
    await state.update_data(path=path)

    # подгрузим все языки, которые есть в словаре
    excel_reader = pd.ExcelFile(path, engine="openpyxl")
    langs = excel_reader.sheet_names
    print(langs)

    # inline buttons с выбором языка из словаря пользователя
    await call.message.edit_media(
        media=input_image,
        reply_markup=builders.builder_many_choose_lang_after_train(
            langs, training)
    )


@router.callback_query(builders.ActionLang.filter(F.action.in_(["eng_to_rus", "translation"])))
async def eng_to_rus(call: CallbackQuery, callback_data: builders.ActionLang, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    if callback_data.lang.endswith('_base'):
        # await state.set_state(Path.path)
        # await state.update_data(path='./data/words.xlsx')
        path='./secret/words.xlsx'
        image = FSInputFile(f"./data/{theme}/packs.png")
    else:
        image = FSInputFile(f"./data/{theme}/your_dict.png")

    await state.set_state(Path.sheet)
    await state.update_data(sheet=callback_data.lang)
    sheet = await state.get_data()
    # await state.set_state(Path.path)
    # path = await state.get_data()

    if callback_data.lang.endswith('_base'):
        sheet = 'Sheet1'
    else:
        print('<<<<<', list(sheet.values()), '<<', list(sheet.values())[1])
        sheet = list(sheet.values())[1]
        

    
    input_image = InputMediaPhoto(media=image)

    await call.message.edit_media(
        media=input_image,
        inline_message_id=call.inline_message_id,
        # reply_markup=builders.inline_keyboard_packs(
        #     list(path.values())[0], sheet, fl='eng_to_rus')
        reply_markup=builders.inline_keyboard_packs(
            path, sheet, fl='eng_to_rus')
    )


@router.callback_query(builders.ActionLang.filter(F.action.in_(["rus_to_eng", "reverse_tran"])))
async def rus_to_eng(call: CallbackQuery, callback_data: builders.ActionLang, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    if callback_data.lang.endswith('_base'):
        # await state.set_state(Path.path)
        # await state.update_data(path='./data/words.xlsx')
        path='./secret/words.xlsx'
        image = FSInputFile(f"./data/{theme}/packs.png")
    else:
        image = FSInputFile(f"./data/{theme}/your_dict.png")

    await state.set_state(Path.sheet)
    await state.update_data(sheet=callback_data.lang)
    sheet = await state.get_data()
    # await state.set_state(Path.path)
    # path = await state.get_data()
    # print('path', list(path.values())[0], 'sheet', list(sheet.values())[1])

    if callback_data.lang.endswith('_base'):
        sheet = 'Sheet1'
    else:
        sheet = list(sheet.values())[1]

    input_image = InputMediaPhoto(media=image)
    # await call.message.answer_photo(
    #     image,
    #     caption=f"translations... good! let's choose a pack",
    #     reply_markup=builders.inline_keyboard_packs(fl='eng_to_rus')
    # )
    await call.message.edit_media(
        media=input_image,
        inline_message_id=call.inline_message_id,
        # reply_markup=builders.inline_keyboard_packs(
        #     list(path.values())[0], sheet, fl='rus_to_eng')
        reply_markup=builders.inline_keyboard_packs(
            path, sheet, fl='rus_to_eng')
    )


@router.callback_query(builders.ActionLang.filter(F.action.in_(["match", "fill_blank"])))
async def start_training(call: CallbackQuery, callback_data: builders.ActionLang, state: FSMContext):
    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    if callback_data.lang.endswith('_base'):
        # await state.set_state(Path.path)
        # await state.update_data(path='./data/words.xlsx')
        path='./secret/words.xlsx'
        image = FSInputFile(f"./data/{theme}/packs.png")
    else:
        image = FSInputFile(f"./data/{theme}/your_dict.png")

    await state.set_state(Path.sheet)
    await state.update_data(sheet=callback_data.lang)
    sheet = await state.get_data()
    # await state.set_state(Path.path)
    # path = await state.get_data()
    # print('path', list(path.values())[0], 'sheet', list(sheet.values())[1])

    if callback_data.lang.endswith('_base'):
        sheet = 'Sheet1'
    else:
        sheet = list(sheet.values())[1]

    input_image = InputMediaPhoto(media=image)
    # await call.message.answer_photo(
    #     image,
    #     caption=f"translations... good! let's choose a pack",
    #     reply_markup=builders.inline_keyboard_packs(fl='eng_to_rus')
    # )
    await call.message.edit_media(
        media=input_image,
        inline_message_id=call.inline_message_id,
        # reply_markup=builders.inline_keyboard_packs(
        #     list(path.values())[0], sheet, fl='match')
        reply_markup=builders.inline_keyboard_packs(
            path, sheet, fl='match')
    )



# нереализованные (пока) фичи
@router.callback_query(builders.ActionLang.filter(F.action == "music"))
async def start_training(call: CallbackQuery, callback_data: inline.Subscriber):
    pass


@router.callback_query(builders.ActionLang.filter(F.action == "videos"))
async def start_training(call: CallbackQuery, callback_data: inline.Subscriber):
    pass


@router.callback_query(builders.ActionLang.filter(F.action == "texts"))
async def start_training(call: CallbackQuery, callback_data: inline.Subscriber):
    pass




# фича с подгрузкой своих слов в словарь
@router.callback_query(builders.TrainThroughLang.filter(F.next_action == "dwnld_words"))
async def start_training(call: CallbackQuery, callback_data: inline.Subscriber):
    # сформированное сообщение с файлом прием файлов добавить слова из файла к выбранному языку (кнопки с
    # существующими языками + кнопка "создать новый язык") -> сделать в packs проверку на количество слов: если до 20
    # слов - без выбора, если больше - выбрать сколько слов: 10, "свое число", все (ххх)
    await call.message.delete()
    msg = "how to do it?\n\n"\
        "1. download the 'example.xlsx' file\n"\
        "2. insert your words and their translations in the appropriate columns\n"\
        "3. send this file after this message"
    file = FSInputFile('./data/example.xlsx')
    await call.message.answer_document(
        file,
        caption=msg,
        reply_markup=builders.to_main_menu_with_del('⬅️ back to menu')
    )


@router.message(F.document)
async def receive_xlsx(message: Message, bot: Bot):
    file = message.document
    await bot.download(file, "./data/userdata/file_from_user.xlsx")
    df = pd.read_excel("./data/userdata/file_from_user.xlsx")
    try:
        global dfr
        dfr = pd.DataFrame(df)

        if await db_does_dict_exists(message.from_user.id):
            excel_reader = pd.ExcelFile(
                f'./data/userdata/dict_{message.from_user.id}.xlsx')
            langs = excel_reader.sheet_names
            txt_for_lang_btns = []
            for i in langs:
                txt_for_lang_btns.append(i)
            print(txt_for_lang_btns)
            calls_for_lang_btns = []
        else:

            # new_dict = pd.DataFrame()
            # new_dict.to_excel(f'./data/dict_{message.from_user.id}.xlsx')
            await db_update_dict(message.from_user.id)
            txt_for_lang_btns = []
            calls_for_lang_btns = []

        for i in txt_for_lang_btns:
            calls_for_lang_btns.append(
                '_'.join([j.strip() for j in i.split(' ')]) + '_lang_call')
        global calls
        calls = calls_for_lang_btns
        print(calls_for_lang_btns)

        await message.answer(
            'what language is it?',
            reply_markup=builders.builder_many_lang(
                txt_for_lang_btns, calls_for_lang_btns)
        )

    except KeyError:
        await message.answer(
            "it seems that you have changed the columns's names. try again but keep columns' names as in example"
        )


@router.callback_query(F.data.endswith('_lang_call'))
async def receive_lang_call(call: CallbackQuery):
    lang = call.data.split(':')[1].strip('_lang_call')
    print(lang)
    global dfr
    if os.path.exists(f'./data/userdata/dict_{call.from_user.id}.xlsx'):
        dfr.to_excel(
            f'./data/userdata/dict_{call.from_user.id}.xlsx',
            sheet_name=f'{lang}'
        )
    else:
        with open(f'./data/userdata/dict_{call.from_user.id}.xlsx', "x") as file:
            dfr.to_excel(
                file,
                sheet_name=f'{lang}'
            )
            file.close()
    await call.message.answer(
        'your words have added to a dictionary'
    )
    sleep(2)
    print(call.message.from_user.id)
    await main_menu(call.message)


@router.callback_query(builders.UserCommand.filter(F.action == 'add_lang'))
async def receive_add_lang_call(call: CallbackQuery):
    await call.message.answer(
        'write a new language name below'
    )


@router.message(F.text)
async def add_new_lang(message: Message):
    lang = message.text
    print(lang)
    global dfr
    dfr.to_excel(
        f'./data/userdata/dict_{message.from_user.id}.xlsx',
        sheet_name=f'{lang}', index=None
    )
    await message.answer(
        f'your dictionary now has a new language - "{lang}". your words have added there'
    )
    sleep(2)
    await main_menu(message)




# фича с выбором рандомных слов из кембриджского словаря
# и возможностью сохранения их в собственный словарь
@router.callback_query(builders.TrainThroughLang.filter(F.train == "random"))
async def start_training(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    try:
        ms = await call.message.answer(
            text='searching for a word...',
            reply_markup=builders.try_again()
        )
        print('💎')
        resourse = cambridge_dict_find_word()
        msg, data = resourse[0], resourse[1]
        await state.set_state(Dictionary.ddata)
        await state.update_data(ddata=data)
        print('>>>>>>>>>>', data)
        path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
        await ms.edit_text(
            text=msg,
            reply_markup=builders.random_kb(path, data)
        )
    except ConnectionError:
        await call.message.edit_text(
            text='we cannot connect to dictionary 😭',
            reply_markup=builders.to_main_menu('⬅️ back to menu')
        )


@router.callback_query(builders.DataTransferActionObject.filter(F.action == "save_cambridge"))
async def start_training(call: CallbackQuery, callback_data: builders.DataTransferActionObject, state: FSMContext):
    # data = callback_data.data

    path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
    await state.set_state(Dictionary.ddata)
    d = await state.get_data()
    data = list(d.values())

    print('data to save:', data)

    save_to_cambridge_dict(path, data)

    await call.message.edit_reply_markup(
        reply_markup=builders.random_kb(path, data)
    )


@router.callback_query(builders.DataTransferActionObject.filter(F.action == "unsave_cambridge"))
async def start_training(call: CallbackQuery, callback_data: builders.DataTransferActionObject, state: FSMContext):
    path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
    await state.set_state(Dictionary.ddata)
    d = await state.get_data()
    data = list(d.values())

    print('data to unsave:', data)

    await delete_from_cambridge_dict(path, data, call.from_user.id)

    pnum = await db_settings_get_camb_w_num(call.from_user.id)
    await db_settings_update_camb_w_num(call.from_user.id, int(pnum[0][0])-1)

    if callback_data.action == 'next_word':
        await next_word_func(call, state)
    else:
        await call.message.edit_reply_markup(
            reply_markup=builders.random_kb(path, data)
        )


@router.callback_query(builders.UserCommand.filter(F.action == "next_cambridge"))
async def start_training(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            text='searching for a word...',
            reply_markup=builders.try_again()
        )
    except aiogram.exceptions.TelegramBadRequest:
        await call.message.edit_text(
            text='searching for a word again...',
            reply_markup=builders.try_again()
        )
    path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
    print('❤️')
    resourse = cambridge_dict_find_word()
    msg, data = resourse[0], resourse[1]
    await state.set_state(Dictionary.ddata)
    await state.update_data(ddata=data)
    await call.message.edit_text(
        text=msg,
        reply_markup=builders.random_kb(path, data)
    )




# фича, чтобы просматривать свои слова (именно кембриджского...)
@router.callback_query(builders.TrainThroughLang.filter(F.train == "dictionary"))
async def start_training(call: CallbackQuery):
    await call.message.delete()
    path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
    # await state.set_state(Dictionary.cambridge_word_number)
    data = await cambridge_dict_iterator(path, call.from_user.id)
    msg = f"<b>{data[0]}</b> <i>({data[1]})</i> – {data[2]}\n" \
        f"– {data[3]}\n\n" \
        f"<i>🗣️ examples:</i>\n{data[4]}"

    await call.message.answer(
        text=msg,
        reply_markup=builders.dict_kb(path, data)
    )


@router.callback_query(builders.UserCommand.filter(F.action == "next_word"))
async def next_word_func(call: CallbackQuery):
    path = f'./data/userdata/cambridge_dict_{call.from_user.id}.xlsx'
    # await state.set_state(Dictionary.cambridge_word_number)
    data = await cambridge_dict_iterator(path, call.from_user.id)
    msg = f"<b>{data[0]}</b> <i>({data[1]})</i> – {data[2]}\n" \
        f"– {data[3]}\n\n" \
        f"<i>🗣️ examples:</i>\n{data[4]}"

    await call.message.edit_text(
        text=msg,
        reply_markup=builders.dict_kb(path, data)
    )