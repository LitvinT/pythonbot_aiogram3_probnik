from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DECIMAL, select, Boolean, BigInteger, SmallInteger, \
    TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, join

from loader import DATABASE_URL

Base = declarative_base()


class BaseMixin(object):
    id = Column(Integer, primary_key=True)

    engine = create_async_engine(f'postgresql+asyncpg://{DATABASE_URL}')

    def __init__(self, **kwargs) -> None:
        for kw in kwargs.items():
            self.__getattribute__(kw[0])
            self.__setattr__(*kw)

    @staticmethod
    def create_async_session(func):
        async def wrapper(*args, **kwargs):
            async with AsyncSession(bind=BaseMixin.engine) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @create_async_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_async_session
    async def get(cls, pk: int, session: AsyncSession = None) -> Base:
        return await session.get(cls, pk)

    @classmethod
    @create_async_session
    async def all(cls, order_by: str = 'id', session: AsyncSession = None, **kwargs) -> list[Base]:
        return [obj[0] for obj in await session.execute(select(cls).filter_by(**kwargs).order_by(order_by))]

    @create_async_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()

    @classmethod
    @create_async_session
    async def join(cls, right: Base, session: AsyncSession = None, **kwargs) -> list[tuple[Base, Base]]:
        return await session.execute(join(left=cls, right=right).filter_by(**kwargs))


class Category(BaseMixin, Base):
    __tablename__: str = 'categories'

    name = Column(VARCHAR(32), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Product(BaseMixin, Base):
    __tablename__: str = 'products'

    article = Column(VARCHAR(128), unique=True, nullable=False)
    brand_id = Column(SmallInteger, ForeignKey('brands.id', ondelete='CASCADE'), nullable=False)
    name = Column(VARCHAR(128), nullable=False)
    model_id = Column(Integer, ForeignKey('models.id', ondelete='CASCADE'), nullable=False)
    title = Column(VARCHAR(256), nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    is_published = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    sex_id = Column(SmallInteger, ForeignKey('sex.id', ondelete='CASCADE'), nullable=True)
    # sex_id = nullable=True

    def __str__(self):
        return self.title

    async def sizes(self) -> list["ProductSize"]:
        return await ProductSize.all(product_id=self.id)

    async def images(self) -> list["ProductImage"]:
        return await ProductImage.all(product_id=self.id)


class ProductSize(BaseMixin, Base):
    __tablename__: str = 'product_sizes'

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size = Column(VARCHAR(10), nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    sex_id = Column(SmallInteger, ForeignKey('sex.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return self.size


class Role(BaseMixin, Base):
    __tablename__: str = 'roles'

    id = Column(SmallInteger, primary_key=True)
    role = Column(VARCHAR(10), unique=True, nullable=False)

    def __str__(self):
        return self.role

    async def users(self) -> list['User']:
        return await User.all(role_id=self.id)


class User(BaseMixin, Base):
    __tablename__: str = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    role_id = Column(SmallInteger, ForeignKey('roles.id', ondelete='NO ACTION'), nullable=True)

    def __str__(self):
        return self.id

    async def role(self):
        return await Role.get(primary_key=self.role_id)

    async def orders(self) -> list['Order']:
        return await Order.all(user_id=self.id)


class OrderStatus(BaseMixin, Base):
    __tablename__: str = 'order_statuses'

    id = Column(SmallInteger, primary_key=True)
    status = Column(VARCHAR(10), unique=True, nullable=False)

    def __str__(self):
        return self.status

    async def orders(self, user_id: int = None) -> list['Order']:
        return await Order.all(**{'status_id': self.id} | {'user_id': user_id} if user_id else {})


class Order(BaseMixin, Base):
    __tablename__: str = 'orders'

    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(SmallInteger, ForeignKey('order_statuses.id', ondelete='NO ACTION'), nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), default=datetime.utcnow())

    async def items(self) -> list['OrderItem']:
        return await OrderItem.all(order_id=self.id)


class OrderItem(BaseMixin, Base):
    __tablename__: str = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    count = Column(SmallInteger, nullable=False, default=1)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='NO ACTION'), nullable=False)
    product_size_id = Column(Integer, ForeignKey('product_sizes.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return self.count


class Brand(BaseMixin, Base):
    __tablename__: str = 'brands'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(64), unique=True, nullable=False)


    def __str__(self):
        return self.name


class Model(BaseMixin, Base):
    __tablename__: str = 'models'

    name = Column(VARCHAR(128), nullable=False, unique=True)
    brand_id = Column(SmallInteger, ForeignKey('brands.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return self.name

    async def brand(self) -> Brand:
        return await Brand.get(primary_key=self.brand_id)

    async def products(self) -> list['Product']:
        return await Product.all(model_id=self.id)


class ModelNext(BaseMixin, Base):
    __tablename__: str = 'model_next'

    name = Column(VARCHAR(128), nullable=False, unique=True)
    model_id = Column(SmallInteger, ForeignKey('models.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return self.name

    async def model(self) -> Model:
        return await Model.get(primary_key=self.model_id)


class ProductImage(BaseMixin, Base):
    __tablename__: str = 'product_images'

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    url = Column(VARCHAR(512), nullable=False)
    telegram_id = Column(VARCHAR(512), nullable=True)

    def __str__(self):
        return self.url


class Sex(BaseMixin, Base):
    __tablename__: str = 'sex'

    id = Column(SmallInteger, primary_key=True)
    sex = Column(VARCHAR(15), nullable=False, unique=True)
    is_published = Column(Boolean, default=True, nullable=True)

    def __str__(self):
        return self.sex


class Basket(BaseMixin, Base):
    __tablename__: str = 'baskets'

    id = Column(SmallInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    sex_id = Column(SmallInteger, ForeignKey('sex.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)




# cоздать класс basket для заказов и выбрвть реплай