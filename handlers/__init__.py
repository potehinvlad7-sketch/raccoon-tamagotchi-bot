from aiogram import Dispatcher

from .admin import router as admin_router
from .menu import router as menu_router
from .start import router as start_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(menu_router)
