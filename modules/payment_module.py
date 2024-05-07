from datetime import timedelta, date, datetime
from time import sleep

from aiogram import Router, F, Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message, FSInputFile, SuccessfulPayment, \
    successful_payment, InlineKeyboardMarkup, InlineKeyboardButton

from config_reader import config
from handlers.user_commands import main_menu_call_1, main_menu_call_4, start
from keyboards import inline
from keyboards.inline import UserCommand as iucmnd
from modules.premium_module import apply_premium
from utils.database import db_settings_get_theme, db_update_pro, db_check_pro, db_settings_get_data

global checkpoint
router = Router()
sub_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='❌ отменить', callback_data='deny_pro'),
            InlineKeyboardButton(text='✅ оплатить', callback_data='get_pro')
        ]
    ]
)


class PaymentStateClass(StatesGroup):
    is_transaction_processing = State()


@router.callback_query(iucmnd.filter(F.action == 'payment'))
async def create_payment_1(call: CallbackQuery, bot: Bot, state: FSMContext):
    
    print(call.message.chat.id)
    check = await db_check_pro(call.message.chat.id)
    print(check)
    await state.set_state(PaymentStateClass.is_transaction_processing)
    if check[0]:
        await call.message.delete()
        # set_data = await db_settings_get_data(call.from_user.id)
        # theme = set_data[0]
        theme = await db_settings_get_theme(call.from_user.id)

        td = timedelta(days=31)
        d = datetime.strptime(check[1][0], '%Y-%m-%d').date()
        expire_date = date.fromisoformat(str(d+td)).strftime("%d of %B %Y, %A")
        image = FSInputFile(f'/home/topg/langbot/langbot-repo/data/{theme}/subscription.png')
        day = date.fromisoformat(str(d)).strftime("%d of %B %Y, %A")
        if day[0] == '0':
            day = day[1:]
        if expire_date[0] == '0':
            expire_date = expire_date[1:]
        await call.message.answer_photo(
            image,
            caption=f'your premium subscription will expire on the {day}\n'
                    f'do you want to extend it till the {expire_date}?',
            reply_markup=inline.expand_or_stop_premium
        )
    
    elif check[1] is not None:
        await call.message.delete_reply_markup()
        global checkpoint
        checkpoint = 'get'
        await bot.send_invoice(
            chat_id=call.message.chat.id,
            title="premium subscription",
            description="unlock advanced features of bot to learn in faster in more creative ways!",
            payload="payment through bot",
            provider_token=config.payment_token.get_secret_value(),
            start_parameter='sdfeghjk',
            currency="RUB",
            prices=[
                LabeledPrice(
                    label="premium subscription",
                    amount=9000,
                    # currency="RUB",
                    # description="unlock advanced features of bot for boosting your skills"
                )
            ],
            max_tip_amount=100000,
            suggested_tip_amounts=[5000, 10000, 20000, 50000],
            # provider_data="Boosty.to",
            # photo_url="https://boosty.to/iamgeorge/boosty.png",
            # photo_size=2048,
        )
    elif check[1] is None:
        await call.message.answer(
            # text="it's your first time! 😍"
            text="let's boost next 30 days with free trial 🚀",
            reply_markup=inline.trial_kb
        )


@router.callback_query(F.data == 'get_pro')
async def create_payment_2(call: CallbackQuery, bot: Bot, state: FSMContext):
    global checkpoint
    checkpoint = 'extend'
    await call.message.delete_reply_markup()
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title="premium subscription",
        description="unlock advanced features of bot to learn in faster in more creative ways!",
        payload="payment through bot",
        provider_token=config.payment_token.get_secret_value(),
        start_parameter='lskrneer',
        currency="RUB",
        prices=[
            LabeledPrice(
                label="premium subscription",
                amount=9000,
                # currency="RUB",
                # description="unlock advanced features of bot for boosting your skills"
            )
        ],
        max_tip_amount=100000,
        suggested_tip_amounts=[5000, 10000, 20000, 50000],
        # provider_data="Boosty.to",
        # photo_url="https://boosty.to/iamgeorge/boosty.png",
        # photo_size=2048,
    )
    
    
@router.callback_query(F.data == 'get_trial')
async def create_payment_2(call: CallbackQuery, bot: Bot, state: FSMContext):
    global checkpoint
    checkpoint = 'get'
    await call.message.delete_reply_markup()
    
    await db_update_pro(checkpoint, call.from_user.id)
    
    print("----------------", call.from_user.id, call.message.from_user.id, call.message.chat.id, "----------------")
    
    msg = f'enjoy the upgraded powers⚡️'
    theme = await db_settings_get_theme(call.from_user.id)
    image = FSInputFile(f'/home/topg/langbot/langbot-repo/data/{theme}/successful_payment.png')
    await call.message.answer_photo(
        image,
        caption=msg
    )
    
    sleep(1)
    await call.message.answer(
        text='now the new main menu will appear'
    )
    sleep(1)
    await call.message.answer(
        text='3'
    )
    sleep(1)
    await call.message.answer(
        text='2'
    )
    sleep(1)
    await call.message.answer(
        text='1'
    )
    sleep(1)
    await call.message.answer(
        text='are you ready for a miracle?'
    )
    sleep(1)
    image = FSInputFile(f"/home/topg/langbot/langbot-repo/data/{theme}/main_menu.png")
    await call.message.answer_photo(
        image,
        # caption=f"you are in main menu ⚡️",
        reply_markup=inline.main_menu_pro
    )


@router.callback_query(F.data == 'deny_pro')
async def create_payment_2(call: CallbackQuery, bot: Bot):
    await call.message.delete_reply_markup()
    await call.message.answer(
        text='okey, enjoy your powers'
    )
    await start(call.message)


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    print('pre')
    await state.update_data(is_transaction_processing=True)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(successful_payment.SuccessfulPayment)


# @router.message(content_types=ContentType.SUCCESSFUL_PAYMENT)
# @router.message(F.data == successful_payment.SuccessfulPayment)
@router.message()
async def process_successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    fact = list(data.values())[0]
    print("data:", data, "or", list(data.values())[0])
    if fact:
        # set_data = await db_settings_get_data(message.from_user.id)
        # theme = set_data[0]
        theme = await db_settings_get_theme(message.from_user.id)

        await state.set_state(PaymentStateClass.is_transaction_processing)
        await state.update_data(is_transaction_processing=False)
        print('successful_payment')
        global checkpoint
        await db_update_pro(checkpoint, message.from_user.id)
        print('сейчас придет письмо')
        msg = f'вы оплатили подписку на сумму {message.successful_payment.total_amount / 100} р.'
        image = FSInputFile(f'/home/topg/langbot/langbot-repo/data/{theme}/successful_payment.png')
        await message.answer_photo(
            image,
            caption=msg
        )
        await apply_premium(message)
