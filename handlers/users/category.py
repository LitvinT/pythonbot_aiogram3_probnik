from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.users import category_paginator_ikb, brand_paginator_ikb
from keyboards.inline.users.general import UserCallbackData

user_category_router = Router(name='user_category')


@user_category_router.callback_query(UserCallbackData.filter((F.target == 'category') & (F.action == 'page')))
async def paginate_categories(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.edit_text(
        text='ВЫБЕРИТЕ КАТЕГОРИЮ',
        reply_markup=await category_paginator_ikb(callback_data=callback_data)
    )


@user_category_router.callback_query(UserCallbackData.filter((F.target == 'category') & (F.action == 'get')))
async def get_category_products(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.edit_text(
        text='ВЫБЕРИТЕ БРЕНД',
        reply_markup=await brand_paginator_ikb(callback_data=callback_data)
    )
