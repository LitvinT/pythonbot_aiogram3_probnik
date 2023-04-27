from models import Category, Sex, Brand, Model, Product, ProductImage, ProductSize, Role, User, OrderStatus, Order,\
    OrderItem
from utils import parse_stockx


# async def main():
#     # await parse_stockx(category='sneakers')
#     categories = ['shoes']
#     for category in categories:
#         category = Category(name=category, is_published=True)
#         await category.save()

#
# async def main():
#     sexi = ['41', '42', '43']
#     for sex in sexi:
#         sex = Sex(sex=sex, is_published=True)
#         await sex.save()


# async def main():
#     br = ['ЗАДАТЬ ВОПРОС', 'ХОЧУ КУПИТЬ ОБОРУДОВАНИЕ', 'КАЛЬКУЛЯТОР ДОХОДНОСТИ', 'ИНДИВИДУАЛЬНАЯ КОНСУЛЬТАЦИЯ']
#     for a in br:
#         a = Brand(name=a)
#         await a.save()


# async def main():
#     N = ['КАЛЬКУЛЯТОР ДОХОДНОСТИ', 'НУЖНА КОНСУЛЬТАЦИЯ', 'ДА, Я ЗНАЮ НУЖНУЮ МОЩЬНОСТЬ']
#     for n in N:
#         n = Model(name=n, brand_id=4)
#         await n.save()


# async  def main():
#     n = Model(
#         name=,
#         brand_id=,
#     )
#1 /article='' Sneakers Shoes


# async def main():
#     N = ['Air Jordan VI?']
#     for n in N:
#         n = Product(
#             name=n,
#             brand_id=5,
#             model_id=18,
#             price=999,
#             category_id=2,
#             sex_id=4,
#             article='L, Shoes jord6/',
#             title=' Air Jordan VI, Shoes,(L)  ',
#             rating=10
#             )
#         await n.save()

# async def main():
#     N = ['https://sneakerfreak.ru/wp-content/uploads/2021/09/Air-Jordan-6-UNC-University-Blue-CT8529-410-Release-Date-On-Feet-scaled.jpg']
#     for n in N:
#         n = ProductImage(
#             product_id=106,
#             url=n
#         )
#         await n.save()


# async def main():
#     N = ['Размер']
#     for n in N:
#         n = ProductSize(
#             product_id=104,
#             size=n,
#             price=989,
#             sex_id=2
#         )
#         await n.save()

# async def main():
#     N = ['izir']
#     for n in N:
#         n = Role(
#             role=n,
#         )
#         await n.save()

# async def main():
#     n = Sex(
#         sex=' НАЖМИ СЮДА'
#     )
#     await n.save()
#
# async def main():
#     N = ['Admin']
#     for n in N:
#         n = OrderStatus(
#             status=n
#         )
#         await n.save()

# async def main():
#     n = Category(
#         name='привет '
#     )
#     await n.save()

# async def main():
#     n = OrderItem(
#         order_id=1,
#         product_id=104,
#         product_size_id=1
#     )
#     await n.save()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
