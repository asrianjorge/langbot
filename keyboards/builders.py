import os.path
from math import ceil
import asyncio

import openpyxl
import pandas as pd
from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data.subloader import get_xlsx
from modules.table_module import does_word_exists_in_dict, cambridge_dict_first_set
from utils.states import Dictionary

router = Router()


class UserCommand(CallbackData, prefix="usrcmnd2"):
    action: str


def train_words():
    df = get_xlsx("data.xlsx")
    num_packs = len(df.columns.to_list()) // 2
    num_pages = ceil(num_packs / 9)

    for num in range(1, num_packs + 1):
        print(df.loc[0:100, f'w{num}':f't{num}'].values.tolist())
    items = [str(i) for i in range(1, num_packs + 1)]

    builder = InlineKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(*[3] * 3)

    return builder


class Builder(CallbackData, prefix="bu"):
    statt: str


def builder_one(text: str, clbk_data: str):
    buildr = InlineKeyboardBuilder()

    buildr.button(text=text, callback_data=Builder(statt=clbk_data).pack())

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


def builder_many(text: list, clbk_data: list):
    buildr = InlineKeyboardBuilder()

    for i in range(len(text)):
        buildr.button(text=text[i], callback_data=Builder(statt=clbk_data[i]))

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int = 0):
    builder = train_words()
    builder.row(
        InlineKeyboardButton(
            text="<-", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(
            text="->", callback_data=Pagination(action="next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


class Pack(CallbackData, prefix="pac"):
    action: str
    number: int
    lang: str
    path: str
    sheet: str


def inline_keyboard_packs(path: str, sheet: str, fl: str):
    nums = []
    
    if 'words' in path:
        df = pd.read_excel(path, sheet_name=sheet)
        num_packs = len(df.columns.to_list()) // 8
    else:
        wb = openpyxl.load_workbook(path)
        sheet1 = wb[sheet]
        col = sheet1['A']
        # num_packs = len(col) // 10 + int(len(col) - (len(col) // 10) > 0)
        if len(col)-1 <= 10:
            nums = [len(col)-1]
        elif 20 >= len(col)-1 > 10:
            nums = [10, len(col)-1]
        else:
            nums = [10, 20]

    builder = InlineKeyboardBuilder()

    if fl == 'match':
        actn = 'match'
    else:
        actn = 'pack'

    if nums == []:
        [builder.button(text=f'pack #{num}', callback_data=Pack(action=actn, number=num, lang=fl, path=path, sheet=sheet)) for num in
        range(1, num_packs + 1)]
        builder.adjust(*[4])
    else:
        print(">>>>", int(f'-{nums[0]}'), isinstance(int(f'-{nums[0]}'), int))
        print(actn, fl, sheet, path)
        [builder.button(text=f'{num} random words', callback_data=Pack(action=actn, number=int(f"-{num}"), lang=fl, path=path, sheet=sheet)) for num in nums]
        builder.adjust(*[1])

    # builder.button(text="mix", callback_data=Pack(action='mix', number=0))
    # builder.button(text="things worth learning", callback_data=Pack(action='wrong', number=-1))
    
    builder.row(
        InlineKeyboardButton(
            text="⬅️ back to menu", callback_data=UserCommand(action='main_menu').pack())
    )
    # builder.button(text="⬅️ back to menu", callback_data=UserCommand(action='main_menu').pack())

    return builder.as_markup()


class PaginationNext(CallbackData, prefix="pagnext"):
    action: str
    num: int
    pak: int


def paginator_next(num, packk, flag=False):
    if packk < 0:
        comparator = abs(packk)
    else:
        comparator = 10
    builder = InlineKeyboardBuilder()
    if num < 4:
        builder.row(
            InlineKeyboardButton(text="💡 hint",
                                 callback_data=PaginationNext(action="hint", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    elif num == 4:
        builder.row(
            InlineKeyboardButton(text="💡 hint",
                                 callback_data=PaginationNext(action="hint", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
        builder.row(
            InlineKeyboardButton(text="❌️ tired? quit",
                                 callback_data=PaginationNext(action="quit", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="🚀 till the end",
                                 callback_data=PaginationNext(action="end", num=num, pak=packk).pack())
        )
    elif num == comparator-1:
        builder.row(
            InlineKeyboardButton(text="💡 hint",
                                 callback_data=PaginationNext(action="hint", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="finish ✅",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    elif num > 4 and not flag:
        builder.row(
            InlineKeyboardButton(text="💡 hint",
                                 callback_data=PaginationNext(action="hint", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
        builder.row(
            InlineKeyboardButton(text="❌️ tired? quit",
                                 callback_data=PaginationNext(action="quit", num=num, pak=packk).pack())
        )
    else:
        builder.row(
            InlineKeyboardButton(text="💡 hint",
                                 callback_data=PaginationNext(action="hint", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    return builder.as_markup()


def paginator_next_ru(num, packk, flag=False):
    builder = InlineKeyboardBuilder()
    if num < 4:
        builder.row(
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    elif num == 4:
        builder.row(
            InlineKeyboardButton(text="❌️ tired? quit",
                                 callback_data=PaginationNext(action="quit", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
        builder.row(
            InlineKeyboardButton(text="🚀 till the end",
                                 callback_data=PaginationNext(action="end", num=num, pak=packk).pack())
        )
    elif num == 9:
        builder.row(
            InlineKeyboardButton(text="finish ✅",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    elif num > 4 and not flag:
        builder.row(
            InlineKeyboardButton(text="❌️ tired? quit",
                                 callback_data=PaginationNext(action="quit", num=num, pak=packk).pack()),
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    else:
        builder.row(
            InlineKeyboardButton(text="➡️ next word",
                                 callback_data=PaginationNext(action="next", num=num, pak=packk).pack())
        )
    return builder.as_markup()


def to_main_menu(text):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=text, callback_data=UserCommand(
            action='to_main_menu').pack())
    )
    return builder.as_markup()


def to_main_menu_with_del(text):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=text, callback_data=UserCommand(
            action='to_main_menu_with_del').pack())
    )
    return builder.as_markup()


def builder_many_lang(text: list, clbk_data: list):
    buildr = InlineKeyboardBuilder()

    for i in range(len(text)):
        buildr.button(text=text[i], callback_data=Builder(statt=clbk_data[i]))
    buildr.adjust(*[2])
    buildr.button(text="+ add new language",
                  callback_data=UserCommand(action='add_lang').pack())

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


def builder_many_choose_lang(text: list, clbk_data: list):
    buildr = InlineKeyboardBuilder()

    for i in range(len(text)):
        buildr.button(text=text[i], callback_data=Builder(statt=clbk_data[i]))
    buildr.adjust(*[2])
    buildr.button(text="⬅️ back to menu",
                  callback_data=UserCommand(action='main_menu').pack())

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


class TrainThroughLang(CallbackData, prefix="train_through_lang"):
    train: str
    next_action: str


def train_pro_kb():
    buildr = InlineKeyboardBuilder()

    buildr.button(text='🌐 translation',
                  callback_data=TrainThroughLang(train='translation', next_action='choose_lang').pack())
    buildr.button(text='🔗 reverse translation',
                  callback_data=TrainThroughLang(train='reverse_tran', next_action='choose_lang').pack())
    buildr.button(text='🧠 fill in the blank',
                  callback_data=TrainThroughLang(train='fill_blank', next_action='choose_lang').pack())
    # buildr.button(text='🎧 listen to music', callback_data=TrainThroughLang(train='music', lang=lang).pack())
    # buildr.button(text='🎥 watch videos', callback_data=TrainThroughLang(train='videos', lang=lang).pack())
    # buildr.button(text='📑 read texts', callback_data=TrainThroughLang(train='texts', lang=lang).pack())
    buildr.button(text='🔮 random word',
                  callback_data=TrainThroughLang(train='random', next_action='random').pack())
    buildr.button(text='📕 my dictionary',
                  callback_data=TrainThroughLang(train='dictionary', next_action='dictionary').pack())
    buildr.button(text='📥 download words',
                  callback_data=TrainThroughLang(train='dwnld_words', next_action='dwnld_words').pack())

    buildr.button(text="⬅️ back to menu",
                  callback_data=UserCommand(action='main_menu').pack())
    buildr.adjust(*[1])

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


def train_kb():
    buildr = InlineKeyboardBuilder()

    buildr.button(text='🌐 translation (eng → rus)',
                  callback_data=TrainThroughLang(train='eng_to_rus', next_action='choose_lang').pack())
    buildr.button(text='🌐 translation (rus → eng)',
                  callback_data=TrainThroughLang(train='rus_to_eng', next_action='choose_lang').pack())
    buildr.button(text='🧠 fill in the blank',
                  callback_data=TrainThroughLang(train='match', next_action='choose_lang').pack())
    # buildr.button(text='🎧 listen to music', callback_data=TrainThroughLang(train='music', lang=lang).pack())
    # buildr.button(text='🎥 watch videos', callback_data=TrainThroughLang(train='videos', lang=lang).pack())
    # buildr.button(text='📑 read texts', callback_data=TrainThroughLang(train='texts', lang=lang).pack())
    # buildr.adjust(*[2])
    buildr.button(text="⬅️ back to menu",
                  callback_data=UserCommand(action='main_menu').pack())
    buildr.adjust(*[1])

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


class ActionLang(CallbackData, prefix="act_lang"):
    action: str
    lang: str


def builder_many_choose_lang_after_train(langs: list, train: str):
    buildr = InlineKeyboardBuilder()
    for i in range(len(langs)):
        buildr.button(text=langs[i], callback_data=ActionLang(
            action=train, lang=langs[i]))
    buildr.adjust(*[2])
    buildr.button(text="⬅️ back to menu",
                  callback_data=UserCommand(action='main_menu').pack())

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


def eng_or_my_lang(train: str, flagg: bool):
    buildr = InlineKeyboardBuilder()
    if flagg:
        buildr.row(
            InlineKeyboardButton(text="🇬🇧 english",
                                 callback_data=ActionLang(action=train, lang='english_base').pack()),
            InlineKeyboardButton(text="📕 my language",
                                 callback_data=ActionLang(action=train, lang='my_lang').pack()),
        )
    else:
        buildr.row(
            InlineKeyboardButton(text="🇬🇧 english",
                                 callback_data=ActionLang(action=train, lang='english_base').pack()),
        )
    buildr.row(
        InlineKeyboardButton(text="⬅️ back to menu",
                             callback_data=UserCommand(action='main_menu').pack()),
    )

    return buildr.as_markup(resize_keyboard=True, one_time_keyboard=True)


class DataTransferActionObject(CallbackData, prefix="data_trans_act_obj"):
    action: str
    data: str


def random_kb(path, data):
    random_kb_builder = InlineKeyboardBuilder()

    if not os.path.exists(path):
        cambridge_dict_first_set(path, Dictionary.cambridge_word_number)

    try:
        if data == []:
            msg = '📕 save'
            act = 'next_cambridge'
        elif isinstance(data[0], str) and does_word_exists_in_dict(data[0], path) or isinstance(data[0][0], str) and does_word_exists_in_dict(data[0][0], path) or isinstance(data[0][0][0], str) and does_word_exists_in_dict(data[0][0][0], path):
            msg = '✅ saved'
            act = 'unsave_cambridge'
        else:
            msg = '📕 save'
            act = 'save_cambridge'
    except FileNotFoundError:
        msg = '📕 save'
        act = 'save_cambridge'

    random_kb_builder.row(
        InlineKeyboardButton(text=msg,
                             callback_data=DataTransferActionObject(action=act, data='next_cambridge').pack()),
        InlineKeyboardButton(text="➡️ next word",
                             callback_data=UserCommand(action='next_cambridge').pack()),
    )
    random_kb_builder.row(
        InlineKeyboardButton(text="❌ quit",
                             callback_data=UserCommand(action='to_main_menu_with_del').pack()),
    )
    return random_kb_builder.as_markup()


def try_again():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔄 try again",
                callback_data=UserCommand(action='next_cambridge').pack()))
    return builder.as_markup()


def dict_kb(path, data):
    random_kb_builder = InlineKeyboardBuilder()

    if not os.path.exists(path):
        cambridge_dict_first_set(path, Dictionary.cambridge_word_number)

    try:
        if data == []:
            msg = '📕 save'
            act = 'next_word'
        elif isinstance(data[0], str) and does_word_exists_in_dict(data[0], path) or isinstance(data[0][0], str) and does_word_exists_in_dict(data[0][0], path):
            msg = '✅ saved'
            act = 'unsave_cambridge'
        else:
            msg = '📕 save'
            act = 'save_cambridge'
    except FileNotFoundError:
        msg = '📕 save'
        act = 'save_cambridge'

    random_kb_builder.row(
        InlineKeyboardButton(text=msg,
                             callback_data=DataTransferActionObject(action=act, data='next_word').pack()),
        InlineKeyboardButton(text="➡️ next word",
                             callback_data=UserCommand(action='next_word').pack()),
    )
    random_kb_builder.row(
        InlineKeyboardButton(text="❌ quit",
                             callback_data=UserCommand(action='to_main_menu_with_del').pack()),
    )
    return random_kb_builder.as_markup()