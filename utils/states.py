from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    is_registered = State('False')
    name = State()
    gender = State()
    level_of_english = State()
    level_of_spanish = State()
    preferred_lang = State()
    goal_english = State()
    goal_spanish = State()


class Achievements(StatesGroup):
    one_hundred_percent = State()
    one_hundred_percent_strike_5 = State()
    one_hundred_percent_strike_30 = State()
    one_hundred_percent_strike_90 = State()
    one_hundred_percent_strike_180 = State()
    one_hundred_percent_strike_365 = State()
    english = State()
    spanish = State()
    energizer = State()
    energizer_strike_5 = State()
    energizer_strike_30 = State()
    energizer_strike_90 = State()
    energizer_strike_180 = State()
    energizer_strike_365 = State()
    movie = State()
    music = State()
    translator = State()


class Settings(StatesGroup):
    theme = State()
    sys_lang = State()


class Dictionary(StatesGroup):
    cambridge_word_number = State()
    ddata = State()


class Temporal(StatesGroup):
    user_id = State()