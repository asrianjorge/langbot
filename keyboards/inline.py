from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Subscriber(CallbackData, prefix="subs"):
    action: str


class UserCommand(CallbackData, prefix="usrcmnd"):
    action: str


subscribe = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="↗️ subscribe",
                                 url="tg://resolve?domain=englishplusspanish"),
            # InlineKeyboardButton(
            #     text="✅ subscribed", callback_data=Subscriber(action='check').pack())
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


class Language(CallbackData, prefix="lan"):
    action: str
    lang: str


lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 english",
                                 callback_data=Language(action='choose_training', lang='english').pack()),
            # InlineKeyboardButton(text="🇪🇸 español", callback_data=Language(action='choose_lang', lang='esp').pack())
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


class Profile(CallbackData, prefix="prof"):
    action: str


reg = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="register 👤", callback_data=Profile(action='register').pack())
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


class Level(CallbackData, prefix="lev"):
    action: str
    answer: str


level = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="A1", callback_data=Level(
                action='reg', answer="A1").pack()),
            InlineKeyboardButton(text="A2", callback_data=Level(
                action='reg', answer="A1").pack()),
            InlineKeyboardButton(text="B1", callback_data=Level(
                action='reg', answer="A1").pack())
        ],
        [
            InlineKeyboardButton(text="B2", callback_data=Level(
                action='reg', answer="A1").pack()),
            InlineKeyboardButton(text="C1", callback_data=Level(
                action='reg', answer="A1").pack()),
            InlineKeyboardButton(text="C2", callback_data=Level(
                action='reg', answer="A1").pack())
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


class Train(CallbackData, prefix="trainn"):
    mode: str


train = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🌐 translation (eng → rus)', callback_data=Train
                                 (mode='eng_to_rus').pack()),
        ],
        [
            InlineKeyboardButton(text='🌐 translation (rus → eng)', callback_data=Train
                                 (mode='rus_to_eng').pack()),
        ],
        [
            InlineKeyboardButton(text='🧠 fill in the blank',
                                 callback_data=Train(mode='match').pack()),
        ],
        # [
        #     InlineKeyboardButton(text='🎧 listen to music', callback_data=Train(mode='music').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='🎥 watch videos', callback_data=Train(mode='videos').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='📑 read texts', callback_data=Train(mode='texts').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='📥 download your words', callback_data=Train(mode='texts').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='🔮 random word', callback_data=Train(mode='texts').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='📕 your dictionary', callback_data=Train(mode='texts').pack()),
        # ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

train_pro = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🌐 translation (eng → rus)',
                                 callback_data=Train(mode='eng_to_rus').pack()),
        ],
        [
            InlineKeyboardButton(text='🌐 translation (rus → eng)',
                                 callback_data=Train(mode='rus_to_eng').pack()),
        ],
        [
            InlineKeyboardButton(text='🧠 fill in the blank',
                                 callback_data=Train(mode='match').pack()),
        ],
        # [
        #     InlineKeyboardButton(text='🎧 listen to music', callback_data=Train(mode='music').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='🎥 watch videos', callback_data=Train(mode='videos').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text='📑 read texts', callback_data=Train(mode='texts').pack()),
        # ],
        [
            InlineKeyboardButton(text='📥 download your words',
                                 callback_data=Train(mode='dwnld_words').pack()),
        ],
        [
            InlineKeyboardButton(text='🔮 random word',
                                 callback_data=Train(mode='random').pack()),
        ],
        [
            InlineKeyboardButton(text='📕 your dictionary',
                                 callback_data=Train(mode='dictionary').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text="🏋️ train", callback_data=UserCommand(action='train').pack()),
        #     InlineKeyboardButton(text="💡 about the bot", callback_data=UserCommand(action='about').pack())
        # ],
        # [
        #     InlineKeyboardButton(text="🏆 achievements", callback_data=UserCommand(action='achievements').pack()),
        #     InlineKeyboardButton(text="💎 premium features", callback_data=UserCommand(action='premium').pack())
        # ],
        # [
        #     InlineKeyboardButton(text="⚡️ community rating", callback_data=UserCommand(action='rating').pack()),
        #     InlineKeyboardButton(text="👤 profile", callback_data=UserCommand(action='profile').pack())
        # ],
        # [
        #     InlineKeyboardButton(text="💟 donate", url='https://boosty.to/iamgeorge/donate'),
        #     InlineKeyboardButton(text="🙋 support", callback_data=UserCommand(action='support').pack())
        # ],

        [
            InlineKeyboardButton(
                text="🏋️ train", callback_data=UserCommand(action='train').pack()),
            InlineKeyboardButton(
                text="💡 about", callback_data=UserCommand(action='about').pack())
        ],
        [
            InlineKeyboardButton(
                text="💟 donate", url='https://boosty.to/iamgeorge/donate'),
            InlineKeyboardButton(
                text="🙋 support", callback_data=UserCommand(action='support').pack())
        ],
        [
            InlineKeyboardButton(
                text="💎 advanced features", callback_data=UserCommand(action='premium').pack())
        ],
    ],
    resize_keyboard=True
)

main_menu_pro = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔥 train", callback_data=UserCommand(action='train').pack()),
            # InlineKeyboardButton(
            #     text="💡 about", callback_data=UserCommand(action='about').pack())
        ],
        # [
        #     InlineKeyboardButton(
        #         text="💟 donate", url='https://boosty.to/iamgeorge/donate'),
        #     InlineKeyboardButton(
        #         text="🙋 support", callback_data=UserCommand(action='support').pack())
        # ],
        [
            InlineKeyboardButton(
                text="⚙️ settings", callback_data=UserCommand(action='settings').pack())
        ]
    ],
    resize_keyboard=True
)

settings_kb_pro = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💡 about", callback_data=UserCommand(action='about').pack())
        ],
        # [
        #     InlineKeyboardButton(
        #         text="🎨 themes", callback_data=UserCommand(action='themes').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text="🇬🇧 system language", 
        #                          callback_data=UserCommand(action='sys_lang').pack()),
        # ],
        [
            InlineKeyboardButton(
                text="💎 my subscribtion", callback_data=UserCommand(action='payment').pack()),
        ],
        [
            InlineKeyboardButton(
                text="💟 donate", url='https://boosty.to/iamgeorge/donate')
        ],
        [
            InlineKeyboardButton(
                text="🙋 support", callback_data=UserCommand(action='support').pack())
        ],
        # [
        #     InlineKeyboardButton(text="ℹ️ how to download words?",
        #                          callback_data=UserCommand(action='how_to_dwnld_words').pack()),
        # ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

themes_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🖤 basic theme', callback_data=UserCommand
                                 (action='basic_theme').pack())
        ],
        [
            InlineKeyboardButton(text='💥 color flash', callback_data=UserCommand
                                 (action='color_flash_theme').pack())
        ],
        # [
        #     InlineKeyboardButton(text='💎 white diamond', callback_data=UserCommand
        #                          (action='white_diamond_theme').pack())
        # ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

about_kb_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 see roadmap", callback_data=UserCommand(action='roadmap').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

about_kb_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💡 about this bot", callback_data=UserCommand(action='about').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

premium_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 get premium",
                                 callback_data=UserCommand(action='payment').pack()),
        ],
        # [
        #     InlineKeyboardButton(text="🔥 white_diamond_theme features", callback_data=UserCommand(action='themes').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text="🔥 pro features",
        #                          callback_data=UserCommand(action='pro_features').pack()),
        #     InlineKeyboardButton(text="🦾 how it works", callback_data=UserCommand
        #                          (action='how_it_works').pack()),
        # ],
        [
            InlineKeyboardButton(text="➡️ next advantages", callback_data=UserCommand(
                action='premium2').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

premium_kb_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 get premium",
                                 callback_data=UserCommand(action='payment').pack()),
        ],
        # [
        #     InlineKeyboardButton(text="🔥 white_diamond_theme features", callback_data=UserCommand(action='themes').pack()),
        # ],
        # [
        #     InlineKeyboardButton(text="🔥 pro features",
        #                          callback_data=UserCommand(action='pro_features').pack()),
        #     InlineKeyboardButton(text="🦾 how it works", callback_data=UserCommand
        #                          (action='how_it_works').pack()),
        # ],
        [
            InlineKeyboardButton(text="⬅️ previous advantages", callback_data=UserCommand(
                action='premium').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

premium_kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 get premium",
                                 callback_data=UserCommand(action='payment').pack()),
        ],
        # [
        #     InlineKeyboardButton(text="🔥 white_diamond_theme features", callback_data=UserCommand(action='themes').pack()),
        # ],
        [
            InlineKeyboardButton(text="💡 about pro",
                                 callback_data=UserCommand(action='premium').pack()),
            InlineKeyboardButton(text="🦾 how it works", callback_data=UserCommand
                                 (action='how_it_works').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

premium_kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 get premium",
                                 callback_data=UserCommand(action='payment').pack()),
        ],
        # [
        #     InlineKeyboardButton(text="🔥 white_diamond_theme features", callback_data=UserCommand(action='themes').pack()),
        # ],
        [
            InlineKeyboardButton(text="💡 about pro",
                                 callback_data=UserCommand(action='premium').pack()),
            InlineKeyboardButton(text="🔥 pro features",
                                 callback_data=UserCommand(action='pro_features').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

lang_kb_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🇬🇧 english", callback_data=UserCommand(action='english').pack()),
            InlineKeyboardButton(
                text="📕 my language", callback_data=UserCommand(action='my_langs').pack()),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='main_menu').pack()),
        ]
    ],
    resize_keyboard=True
)

expand_or_stop_premium = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text="💎 extend subsciption",
        #                          callback_data=UserCommand(action='payment').pack()),
        # ],
        [
            InlineKeyboardButton(text="💎 extend subsciption",
                                 callback_data='get_pro'),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='to_main_menu_with_del').pack()),
        ]
    ],
    resize_keyboard=True
)

trial_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 get 30-days trial",
                                 callback_data='get_trial'),
        ],
        [
            InlineKeyboardButton(text="⬅️ back to menu", callback_data=UserCommand(
                action='to_main_menu_with_del').pack()),
        ]
    ],
    resize_keyboard=True
)