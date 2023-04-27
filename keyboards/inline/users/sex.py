from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Sex
from .general import UserCallbackData


async def sex_ikb() -> InlineKeyboardMarkup:
    objs = await Sex.all(is_published=True)
    objs_iter = iter(objs)
    objs_iter = list(map(list, zip_longest(*([objs_iter]*2))))
    buttons = [
        [
            InlineKeyboardButton(
                text=obj.sex.upper(),
                callback_data=UserCallbackData(
                    target='sex',
                    action='get',
                    sex_id=obj.id
                ).pack()
            )
            for obj in line
            if obj
        ]
        for line in objs_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
