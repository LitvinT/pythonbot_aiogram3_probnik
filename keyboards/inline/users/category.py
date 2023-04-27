from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Category
from .general import UserCallbackData


async def category_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    categories = await Category.all(is_published=True)
    categories_iter = iter(categories)
    categories = list(zip_longest(*([categories_iter] * 5)))
    categories_page = list(filter(lambda x: x, categories[callback_data.category_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text=category.name.upper(),
                callback_data=UserCallbackData(**callback_data.dict() | {
                    'target': 'category',
                    'action': 'get',
                    'category_id': category.id
                }).pack()
            )
        ]
        for category in categories_page
    ]
    if len(categories) > 1:
        if not callback_data.category_page:
            prev_page = len(categories) - 1
        else:
            prev_page = callback_data.category_page - 1

        if callback_data.category_page == len(categories) - 1:
            next_page = 0
        else:
            next_page = callback_data.category_page + 1

        buttons += [
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {'target': 'category', 'action': 'page', 'category_page': prev_page}
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {'target': 'category', 'action': 'page', 'category_page': next_page}
                    ).pack()
                )
            ]
        ]
    buttons += [
        [
            InlineKeyboardButton(
                text='🔙',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'sex',
                        'action': 'all',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
