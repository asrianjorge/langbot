from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="english🇬🇧"),
            KeyboardButton(text="español🇪🇸")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

train = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🌐 translation (eng → rus)')
        ],
        [
            KeyboardButton(text='🌐 translation (rus → eng)')
        ],
        [
            KeyboardButton(text='🧠 match word to its meaning')
        ],
        [
            KeyboardButton(text='🎧 listen to music')
        ],
        [
            KeyboardButton(text='🎥 watch videos')
        ],
        [
            KeyboardButton(text='📑 read texts')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="what will we do?",
    selective=True
)

# train = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="learn words"),
#             KeyboardButton(text="watch videos")
#         ],
#         [
#             KeyboardButton(text="listen to music"),
#             KeyboardButton(text="pass the test (soon)")
#         ]
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True,
#     input_field_placeholder="what will we do?",
#     selective=True
# )

rmk = ReplyKeyboardRemove()

level = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A1"),
            KeyboardButton(text="A2"),
            KeyboardButton(text="B1")
        ],
        [
            KeyboardButton(text="B2"),
            KeyboardButton(text="C1"),
            KeyboardButton(text="C2")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


