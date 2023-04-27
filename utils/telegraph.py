import os
from json import loads

from aiofiles import open as aiopen

from loader import telegraph, BASE_DIR
from models import Product


async def create_page(product: Product) -> str:
    async with aiopen(os.path.join(BASE_DIR, 'product_detail.html'), 'r', encoding='utf-8') as file:
        html = await file.read()
    page = await telegraph.create_page(
        title=product.title,
        html_content=html.format(
            photo_url=product.photo_url,
            title=product.title,
            descr=product.descr,
            price=product.price
        )
    )
    return page['url']
