from aiogram import Router

from .sex import user_sex_router
from .category import user_category_router
from .brand import user_brand_router
from .model import user_model_router
from .product import user_product_router
from .main_panel import user_main_router


user_router = Router(name='users')
user_router.include_router(router=user_sex_router)
user_router.include_router(router=user_category_router)
user_router.include_router(router=user_brand_router)
user_router.include_router(router=user_model_router)
user_router.include_router(router=user_product_router)
user_router.include_router(router=user_main_router)



__all__: list[str] = [
    'user_router'
]
