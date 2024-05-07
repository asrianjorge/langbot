from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import inline
from utils.states import Form
from keyboards.builders import builder_one, Builder
from keyboards.reply import rmk
from keyboards.inline import level, Subscriber
from aiogram.types import FSInputFile

router = Router()


@router.callback_query(inline.Profile.filter(F.action == "register"))
async def fill_profile(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    print(call.from_user.first_name)
    await call.message.answer(
        text="let's start! enter your name",
        reply_markup=builder_one(call.from_user.first_name, 'name')
    )


@router.callback_query(Builder.filter(F.statt == 'name'))
async def form_name(call: CallbackQuery, state: FSMContext):
    txt = call.text
    # print(f"{call.message} >> {call.message.text} >> {call.data} >> {call.message.caption} >> {call.data}")
    print(txt)
    await state.update_data(name=call.text)
    await state.set_state(Form.level_of_english)
    await call.message.answer(
        f"got it! now pick your level of english",
        reply_markup=level
    )


# @router.message()
# async def form_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Form.level_of_english)
#     await message.answer(
#         f"got it! now pick your level of english",
#         reply_markup=level
#     )


# @router.message(Form.level_of_english, F.text.lower().in_(['a1', 'a2', 'b1', 'b2', 'c1', 'c2']))
@router.callback_query(Form.level_of_english, Subscriber.filter(F.action == 'reg'))
async def form_level_eng(call: CallbackQuery, state: FSMContext):
    await state.update_data(level_of_english=call.message.text)
    await state.set_state(Form.goal_english)
    await call.message.answer(
        f"okey. pick a level of english you want to achieve",
        reply_markup=level
    )


# @router.message(Form.level_of_english)
# async def incorrect_level_eng(message: Message, state: FSMContext):
#     await message.answer('pick a level by pushing one of the buttons, please')


@router.callback_query(Form.goal_english, Subscriber.filter(F.action == 'reg'))
async def form_goal_eng(call: CallbackQuery, state: FSMContext):
    await state.update_data(goal_english=call.message.text)

    await state.set_state(Form.level_of_spanish)
    await call.message.answer(
        f"done✅ and also pick your level of spanish",
        reply_markup=level
    )


# @router.message(Form.goal_english)
# async def incorrect_goal_eng(message: Message, state: FSMContext):
#     await message.answer('pick a level by pushing one of the buttons, please')


@router.callback_query(Form.level_of_spanish, Subscriber.filter(F.action == 'reg'))
async def form_level_esp(call: CallbackQuery, state: FSMContext):
    await state.update_data(level_of_spanish=call.message.text)
    await state.set_state(Form.goal_spanish)
    await call.message.answer(
        f"done✅ and pick a level of spanish you want to achieve",
        reply_markup=level
    )


# @router.message(Form.level_of_spanish)
# async def incorrect_level_esp(message: Message, state: FSMContext):
#     await message.answer('pick a level by pushing one of the buttons, please')


@router.callback_query(Form.goal_spanish, Subscriber.filter(F.action == 'reg'))
async def form_goal_esp(call: CallbackQuery, state: FSMContext):
    await state.update_data(goal_spanish=call.message.text)
    await state.set_state(Form.is_registered)
    await state.update_data(is_registered='True')
    await call.message.answer(
        f"all done✅ good job!",
        reply_markup=rmk
    )
    data = await state.get_data()
    # await state.clear()

    formatted_text = []
    [formatted_text.append(f"{key}: {value}") for key, value in data.items()]
    print(formatted_text)
    photo_file_id = FSInputFile("./data/new_member.png")
    await call.message.answer_photo(
        photo_file_id,
        caption="\n".join(formatted_text),
    )

# @router.message(Form.goal_spanish, ~F.text.lower().in_(['a1', 'a2', 'b1', 'b2', 'c1', 'c2', "english🇬🇧", "español🇪🇸", "learn words", "watch videos", "listen to music", "pass the test (soon)"]))
# async def incorrect_goal_esp(message: Message, state: FSMContext):
#     await message.answer('pick a level by pushing one of the buttons, please')
#
