from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import inline

from handlers.user_commands import start

router = Router()


@router.callback_query(inline.Subscriber.filter(F.action == "check"))
async def check_sub(call: CallbackQuery):
    chat_member = await call.bot.get_chat_member(chat_id="@englishplusspanish", user_id=call.from_user.id)
    if chat_member.status != 'left':
        await start(message=call.message)
    return await call.answer()
