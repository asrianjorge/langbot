from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, FSInputFile

from keyboards.inline import subscribe
from aiogram.fsm.context import FSMContext

from utils.database import db_does_user_exist, db_settings_get_theme

# from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

# from utils.states import Temporal


class CheckSubscription(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id=event.from_user.id
        chat_member = await event.bot.get_chat_member(chat_id="@englishplusspanish", user_id=user_id)
        msg_id = event.message_id
        # await user_determination(event.from_user.id, Temporal.user_id)

        # user_id = event.from_user.id
        # chat_id = event.chat.id
        # state_with: FSMContext = FSMContext(
        #     #bot=bot,  # объект бота
        #     storage=dp.storage,  # dp - экземпляр диспатчера
        #     key=StorageKey(
        #         chat_id=chat_id,  # если юзер в ЛС, то chat_id=user_id
        #         user_id=user_id,
        #         bot_id=bot.id))
        #     await state_with.update_data() # обновить дату для пользователя
        #     await state_with.set_state(quizStates.temp1)  # пример присвоения стейта



        
        if chat_member.status == 'left':
            if db_does_user_exist(user_id):
                theme = await db_settings_get_theme(user_id)
            else:
                theme = 'basic_theme'
            image = FSInputFile(f"./data/{theme}/sub.png")
            await event.answer_photo(
                image,
                caption='subscribe to the channel to start using a bot. if you have already subscribed, click /start',
                reply_markup=subscribe
            )
        else:
            return await handler(event, data)
