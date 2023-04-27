from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Brand
from .general import UserCallbackData


async def brand_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    brands = await Brand.all()
    brands_iter = iter(brands)
    brands = list(zip_longest(*([brands_iter] * 5)))
    brands_page = list(filter(lambda x: x, brands[callback_data.brand_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text=brand.name.upper(),
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'brand',
                        'action': 'get',
                        'brand_id': brand.id
                    }
                ).pack()
            )
        ]
        for brand in brands_page
    ]
    if len(brands) > 1:
        if not callback_data.brand_page:
            prev_page = len(brands) - 1
        else:
            prev_page = callback_data.brand_page - 1

        if callback_data.brand_page == len(brands) - 1:
            next_page = 0
        else:
            next_page = callback_data.brand_page + 1

        buttons += [
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {
                            'target': 'brand',
                            'action': 'page',
                            'brand_page': prev_page
                        }
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {
                            'target': 'brand',
                            'action': 'page',
                            'brand_page': next_page
                        }
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
                        'target': 'category',
                        'action': 'page',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
