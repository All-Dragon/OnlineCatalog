from aiogram import Dispatcher

from app.handlers.admin import admin_router
from app.handlers.start import start_router


dispatcher = Dispatcher(disable_fsm=True)

dispatcher.include_router(start_router)
dispatcher.include_router(admin_router)
