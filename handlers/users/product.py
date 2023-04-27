from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards.inline.users import product_paginator_ikb, product_detail_ikb
from keyboards.inline.users.general import UserCallbackData
from loader import bot
from models import Product, ProductSize

user_product_router = Router(name='user_product')


@user_product_router.callback_query(UserCallbackData.filter((F.target == 'product') & (F.action == 'page')))
async def paginate_category_products(callback: CallbackQuery, callback_data: UserCallbackData):
    try:
        for i in range(1, 8):
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id - i
            )
    except TelegramBadRequest:
        pass
    await callback.message.edit_text(
        text='ВЫБЕРИТЕ ТОВАР',
        reply_markup=await product_paginator_ikb(callback_data=callback_data)
    )


@user_product_router.callback_query(UserCallbackData.filter((F.target == 'product') & (F.action == 'get')))
async def get_category_product(callback: CallbackQuery, callback_data: UserCallbackData):
    try:
        for i in range(1, 8):
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id - i
            )
    except TelegramBadRequest:
        pass
    product = await Product.get(pk=callback_data.product_id)
    if product:
        text = f'''
<b>{product.title.upper()}</b>

<i>Цена:</i> <b>{product.price}$</b>        
'''
        await callback.message.delete()
        images_group = [image for image in await product.images()]
        images = await callback.message.answer_media_group(
            media=[
                InputMediaPhoto(media=photo.telegram_id if photo.telegram_id else photo.url)
                for photo in images_group
            ]
        )
        for i in range(len(images_group)):
            images_group[i].telegram_id = images[i].photo[-1].file_id
            await images_group[i].save()
        await callback.message.answer(
            text=text,
            reply_markup=await product_detail_ikb(callback_data=callback_data),
            disable_web_page_preview=True
        )


@user_product_router.callback_query(UserCallbackData.filter((F.target == 'size') & (F.action == 'get')))
async def get_product_size(callback: CallbackQuery, callback_data: UserCallbackData):
    product = await Product.get(pk=callback_data.product_id)
    product_size = await ProductSize.get(pk=callback_data.size_id)
    await callback.answer(
        text=f'{product.name.upper()}. РАЗМЕР: {product_size.size} ДОБАВЛЕН!'
    )
