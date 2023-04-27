from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Model
from .general import UserCallbackData


async def brand_model_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    if callback_data.brand_id:
        brand_models = await Model.all(order_by='brand_id', brand_id=callback_data.brand_id)
    else:
        brand_models = await Model.all(order_by='brand_id')
    brand_models_iter = iter(brand_models)
    brand_models = list(zip_longest(*([brand_models_iter] * 5)))
    brand_models_page = list(filter(lambda x: x, brand_models[callback_data.brand_model_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text='ВСЕ',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'model',
                        'action': 'get',
                        'model_id': 0
                    }
                ).pack()
            )
        ]
    ]
    buttons += [
        [
            InlineKeyboardButton(
                text=brand_model.name.upper(),
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'model',
                        'action': 'get',
                        'model_id': brand_model.id
                    }
                ).pack()
            )
        ]
        for brand_model in brand_models_page
    ]
    if len(brand_models) > 1:
        if not callback_data.brand_model_page:
            prev_page = len(brand_models) - 1
        else:
            prev_page = callback_data.brand_model_page - 1

        if callback_data.brand_model_page == len(brand_models) - 1:
            next_page = 0
        else:
            next_page = callback_data.brand_model_page + 1

        buttons += [
            [
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {
                            'target': 'model',
                            'action': 'page',
                            'brand_model_page': prev_page
                        }
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data=UserCallbackData(
                        **callback_data.dict() | {
                            'target': 'model',
                            'action': 'page',
                            'brand_model_page': next_page
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
                        'target': 'brand',
                        'action': 'page',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
