from aiogram.filters.callback_data import CallbackData


class UserCallbackData(CallbackData, prefix='user'):
    target: str
    action: str
    ram: str