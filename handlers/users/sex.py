from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from keyboards.inline.users import sex_ikb, category_paginator_ikb
from keyboards.inline.users.general import UserCallbackData

user_sex_router = Router(name='user_sex')


@user_sex_router.message(F.text == '📦 КАТЕГОРИИ')
async def send_sex_ikb(message: Message):
    await message.delete()
    await message.answer(
        text='ВЫБЕРИТЕ ТИП РАЗМЕРА',
        reply_markup=await sex_ikb()
    )


@user_sex_router.callback_query(UserCallbackData.filter((F.target == 'sex') & (F.action == 'all')))
async def sex_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text='ВЫБЕРИТЕ ТИП РАЗМЕРА',
        reply_markup=await sex_ikb()
    )


@user_sex_router.callback_query(UserCallbackData.filter((F.target == 'sex') & (F.action == 'get')))
async def get_sex(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.edit_text(
        text='ВЫБЕРИТЕ КАТЕГОРИЮ',
        reply_markup=await category_paginator_ikb(callback_data=callback_data)
    )

