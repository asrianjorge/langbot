from random import randint, shuffle, choice
from time import sleep

import pandas as pd
from aiogram import Router, F
from aiogram.types import CallbackQuery, PollAnswer, FSInputFile

from handlers.user_commands import start
from keyboards import builders
from keyboards.reply import rmk
from utils.database import db_settings_get_data

router = Router()
global correct_answer
global score
global db


# translation training
@router.callback_query(builders.Pack.filter(F.action.in_(["pack", "match"])))
async def packs_handler(call: CallbackQuery, callback_data: builders.Pack):
    global lang
    lang = callback_data.lang
    global score
    score = 0
    global flag
    flag = False

    num = int(callback_data.number)

    # path = "data/words.xlsx"
    path = callback_data.path
    sheet = callback_data.sheet
    df = pd.read_excel(path, sheet_name=sheet)

    global db
    db = []
    try:
        words = df[f'words {num}'].tolist()
        translations = df[f'translations {num}'].tolist()
        explonations1 = df[f'example 1 {num}'].tolist()
        explonations2 = df[f'example 3 {num}'].tolist()
        explonations3 = df[f'example 2 {num}'].tolist()
        why = df[f'meaning {num}'].tolist()
        for j in range(len(words)):
            expl = f'{explonations1[j]} <{explonations3[j]}> {explonations2[j]}'
            if lang == 'eng_to_rus':
                db.append([words[j], translations[j], expl, why[j]])
            elif lang == 'rus_to_eng':
                db.append([translations[j], words[j], expl, why[j]])
            else:
                use_case = f"{explonations1[j]} [...] {explonations2[j]}"
                mnng = f"{explonations1[j]} {explonations3[j]} {explonations2[j]}"
                db.append([why[j], words[j], use_case, mnng])

        await call.message.answer(f"📌 you chose pack #{num}. let's start!")
        await call.message.delete()

    except KeyError:
        num = abs(num)
        words = df[f'words'].tolist()
        translations = df[f'translations'].tolist()
        explonations = df[f'example'].tolist()
        why = df[f'meaning'].tolist()

        db_nums = set()
        while len(db_nums) < num:
            db_nums.add(randint(1, len(words)-1))

        for j in db_nums:
            if lang == 'eng_to_rus':
                db.append([words[j], translations[j], explonations[j], why[j]])
            elif lang == 'rus_to_eng':
                db.append([translations[j], words[j], explonations[j], why[j]])

        await call.message.answer(f"📌 you'll see {num} random words from your dictionary. let's start!")
        await call.message.delete()

    shuffle(db)

    sleep(2)

    word = db[0][0]
    numbers = list(range(1, len(words)))
    x = choice(numbers)
    y = choice(numbers)
    while y == x:
        y = choice(numbers)
    z = choice(numbers)
    while z == y or z == x:
        z = choice(numbers)
    poll_options = [db[0][1], db[x][1], db[y][1], db[z][1]]
    shuffle(poll_options)

    global correct_answer
    correct_answer = poll_options.index(db[0][1])

    if lang == 'eng_to_rus':
        await call.message.answer_poll(
            question=f'translate a word "{word}"',
            options=poll_options,
            is_anonymous=False,
            allows_multiple_answers=False,
            type='quiz',
            correct_option_id=correct_answer,
            explanation=db[0][3],
            is_closed=False,
            id=f'eng_words_pack_{num}_word_{0}',
            total_voter_count=1,
            reply_markup=builders.paginator_next(0, num)
        )
    elif lang == 'rus_to_eng':
        await call.message.answer_poll(
            question=f'find the word using its translation: "{word}"',
            options=poll_options,
            is_anonymous=False,
            allows_multiple_answers=False,
            type='quiz',
            correct_option_id=correct_answer,
            is_closed=False,
            id=f'eng_words_pack_{num}_word_{0}',
            total_voter_count=1,
            reply_markup=builders.paginator_next_ru(0, num)
        )
    else:
        await call.message.answer_poll(
            question=f"fill in the blank with the missing word\n"
                     f"\"{db[0][2]}\"",
            options=poll_options,
            is_anonymous=False,
            allows_multiple_answers=False,
            type='quiz',
            correct_option_id=correct_answer,
            explanation=db[0][3],
            is_closed=False,
            id=f'eng_words_pack_{num}_word_{0}',
            total_voter_count=1,
            reply_markup=builders.paginator_next(0, num)
        )
    print(PollAnswer)

    await call.answer()

    # with suppress(TelegramBadRequest):
    #     await call.message.edit_media(
    #         files=[image_from_pc],
    #         reply_markup=builders.paginator(page)
    #     )
    # await call.poll_answer(poll.Poll(question=f'translate a word "{word}"'))


@router.callback_query(builders.PaginationNext.filter(F.action.in_(["next", "end"])))
async def next_word_handler(call: CallbackQuery, callback_data: builders.PaginationNext):
    global flag
    if callback_data.action == "end":
        flag = True
    num = int(callback_data.pak)

    global db

    i = int(callback_data.num) + 1 if callback_data.num + 1 < len(db) else -1

    if i == -1:
        s = score * 100 // len(db)
        set_data = await db_settings_get_data(call.from_user.id)
        theme = set_data[0]
        rand_color = choice(['_orange', '_pink', '_yellow'])
        if 95 <= s == 100:
            image = FSInputFile(f"./data/{theme}/100{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 85 <= s < 95:
            image = FSInputFile(f"./data/{theme}/90{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 75 <= s < 85:
            image = FSInputFile(f"./data/{theme}/80{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 65 <= s < 75:
            image = FSInputFile(f"./data/{theme}/70{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 55 <= s < 65:
            image = FSInputFile(f"./data/{theme}/60{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 45 <= s < 55:
            image = FSInputFile(f"./data/{theme}/50{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 35 <= s < 45:
            image = FSInputFile(f"./data/{theme}/40{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 25 <= s < 35:
            image = FSInputFile(f"./data/{theme}/30{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 15 <= s < 25:
            image = FSInputFile(f"./data/{theme}/20{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        elif 5 <= s < 15:
            image = FSInputFile(f"./data/{theme}/10{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        else:
            image = FSInputFile(f"./data/{theme}/0{rand_color}.png")
            await call.message.answer_photo(
                image,
                caption=f"the end 🎉\n"
                        f"your score is <b>{s}%</b>",
                reply_markup=builders.to_main_menu('got it 👌')
            )
            # sleep(2)
            # await start(call.message)
        await call.message.delete(id=f'eng_words_pack_{num}_word_{len(db) - 1}')
    else:

        word = db[i][0]
        # ind = first_words.index(word)
        expl = db[i][3]
        numbers = list(range(0, len(db)))
        numbers.remove(i)
        x = choice(numbers)
        y = choice(numbers)
        while y == x:
            y = choice(numbers)
        z = choice(numbers)
        while z == y or z == x:
            z = choice(numbers)
        poll_options = [db[i][1], db[x][1], db[y][1], db[z][1]]
        shuffle(poll_options)

        global correct_answer
        correct_answer = poll_options.index(db[i][1])
        if lang == 'eng_to_rus':
            await call.message.answer_poll(
                question=f'translate a word "{word}"',
                options=poll_options,
                is_anonymous=False,
                allows_multiple_answers=False,
                type='quiz',
                correct_option_id=correct_answer,
                explanation=expl,
                is_closed=False,
                id=f'eng_words_pack_{num}_word_{i}',
                total_voter_count=1,
                reply_markup=builders.paginator_next(i, num, flag)
            )
        elif lang == 'rus_to_eng':
            await call.message.answer_poll(
                question=f'translate a word "{word}"',
                options=poll_options,
                is_anonymous=False,
                allows_multiple_answers=False,
                type='quiz',
                correct_option_id=correct_answer,
                is_closed=False,
                id=f'eng_words_pack_{num}_word_{i}',
                total_voter_count=1,
                reply_markup=builders.paginator_next_ru(i, num, flag)
            )
        else:
            await call.message.answer_poll(
                question=f"fill in the blank with the missing word\n"
                         f"\"{db[i][2]}\"",
                options=poll_options,
                is_anonymous=False,
                allows_multiple_answers=False,
                type='quiz',
                correct_option_id=correct_answer,
                explanation=db[i][3],
                is_closed=False,
                id=f'eng_words_pack_{num}_word_{i}',
                total_voter_count=1,
                reply_markup=builders.paginator_next(i, num, flag)
            )
        await call.message.delete(id=f'eng_words_pack_{num}_word_{i - 1}')
    await call.answer()


@router.callback_query(builders.PaginationNext.filter(F.action == "quit"))
async def quit_handler(call: CallbackQuery, callback_data: builders.PaginationNext):
    num = int(callback_data.pak)
    global db

    set_data = await db_settings_get_data(call.from_user.id)
    theme = set_data[0]

    s = score * 100 // len(db)
    rand_color = choice(['_orange', '_pink', '_yellow'])
    if 95 <= s == 100:
        image = FSInputFile(f"./data/{theme}/100{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is <b>{int(s)}%</b>",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 85 <= s < 95:
        image = FSInputFile(f"./data/{theme}/90{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 75 <= s < 85:
        image = FSInputFile(f"./data/{theme}/80{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 65 <= s < 75:
        image = FSInputFile(f"./data/{theme}/70{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 55 <= s < 65:
        image = FSInputFile(f"./data/{theme}/60{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 45 <= s < 55:
        image = FSInputFile(f"./data/{theme}/50{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 35 <= s < 45:
        image = FSInputFile(f"./data/{theme}/40{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 25 <= s < 35:
        image = FSInputFile(f"./data/{theme}/30{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 15 <= s < 25:
        image = FSInputFile(f"./data/{theme}/20{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    elif 5 <= s < 15:
        image = FSInputFile(f"./data/{theme}/10{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    else:
        image = FSInputFile(f"./data/{theme}/0{rand_color}.png")
        await call.message.answer_photo(
            image,
            caption=f"quiz interrupted 😌\n"
                    f"your score is {int(s)}%",
            reply_markup=builders.to_main_menu('got it 👌')
        )
    await call.message.delete(id=f'eng_words_pack_{num}_word_{len(db) - 1}')


@router.poll_answer()
async def poll_answer_handler(quiz_answer: PollAnswer):
    answer_id = quiz_answer.option_ids[0]

    print(answer_id, correct_answer)

    global score
    if answer_id == correct_answer:
        score += 1

    print(score)


@router.callback_query(builders.PaginationNext.filter(F.action == "hint"))
async def hint_handler(call: CallbackQuery, callback_data: builders.PaginationNext):
    i = int(callback_data.num)

    global db
    why = db[i][2]

    if lang == 'match':
        await call.answer(
            text=f"💡 word's meaning\n\n"
                 f"{db[i][0]}",
            show_alert=True,
        )
    else:
        await call.answer(
            text=f"💡 use case\n\n"
                 f"{why}",
            show_alert=True,
        )
