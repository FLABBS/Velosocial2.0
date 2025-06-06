import sys
import types

# Stub aiogram modules to import handler without installing the dependency
aiogram = types.ModuleType("aiogram")
class DummyRouter:
    def message(self, *a, **k):
        def decorator(f):
            return f
        return decorator
    def callback_query(self, *a, **k):
        def decorator(f):
            return f
        return decorator

aiogram.Router = DummyRouter
class DummyF:
    def __init__(self):
        self.data = types.SimpleNamespace(startswith=lambda *a, **k: None)
        self.location = object()
        self.text = object()
aiogram.F = DummyF()
aiogram.enums = types.ModuleType('aiogram.enums')
class DummyParse:
    HTML = 'HTML'
aiogram.enums.ParseMode = DummyParse
sys.modules['aiogram'] = aiogram
sys.modules['aiogram.enums'] = aiogram.enums
client_mod = types.ModuleType('aiogram.client')
default_mod = types.ModuleType('aiogram.client.default')
class DummyProps:
    def __init__(self, *args, **kwargs):
        pass
default_mod.DefaultBotProperties = DummyProps
client_mod.default = default_mod
sys.modules['aiogram.client'] = client_mod
sys.modules['aiogram.client.default'] = default_mod
fsm = types.ModuleType('aiogram.fsm')
fsm_context = types.ModuleType('aiogram.fsm.context')
fsm_context.FSMContext = object
sys.modules['aiogram.fsm'] = fsm
sys.modules['aiogram.fsm.context'] = fsm_context
types_mod = types.ModuleType('aiogram.types')
types_mod.Message = object
types_mod.CallbackQuery = object
types_mod.InputMediaPhoto = object
sys.modules['aiogram.types'] = types_mod
filters_mod = types.ModuleType('aiogram.filters')
class Command:
    def __init__(self, *a, **k):
        pass
filters_mod.Command = Command
sys.modules['aiogram.filters'] = filters_mod
utils_mod = types.ModuleType('aiogram.utils')
keyboard_mod = types.ModuleType('aiogram.utils.keyboard')
keyboard_mod.InlineKeyboardBuilder = object
utils_mod.keyboard = keyboard_mod
sys.modules['aiogram.utils'] = utils_mod
sys.modules['aiogram.utils.keyboard'] = keyboard_mod
exceptions_mod = types.ModuleType('aiogram.exceptions')
exceptions_mod.TelegramAPIError = Exception
sys.modules['aiogram.exceptions'] = exceptions_mod
aiosqlite_mod = types.ModuleType('aiosqlite')
class DummyConn:
    pass
aiosqlite_mod.Connection = DummyConn
sys.modules['aiosqlite'] = aiosqlite_mod
sys.modules['aiohttp'] = types.ModuleType('aiohttp')

from bot.handlers.map import calculate_bbox


def test_calculate_bbox():
    bbox = calculate_bbox(55.0, 37.0, 5)
    delta = 5 / 111.0
    assert bbox == (55.0 - delta, 55.0 + delta, 37.0 - delta, 37.0 + delta)
