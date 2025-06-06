import sys
import types
import asyncio

# Stub aiogram modules similar to other tests
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
        self.data = types.SimpleNamespace(in_=lambda *a, **k: None)
        self.photo = object()
        self.text = object()
        self.location = object()
aiogram.F = DummyF()
aiogram.enums = types.ModuleType('aiogram.enums')
aiogram.enums.ParseMode = types.SimpleNamespace(HTML='HTML')
sys.modules['aiogram'] = aiogram
sys.modules['aiogram.enums'] = aiogram.enums

client_mod = types.ModuleType('aiogram.client')
default_mod = types.ModuleType('aiogram.client.default')
class DummyProps:
    def __init__(self, *a, **k):
        pass
default_mod.DefaultBotProperties = DummyProps
client_mod.default = default_mod
sys.modules['aiogram.client'] = client_mod
sys.modules['aiogram.client.default'] = default_mod

sys.modules['aiogram.fsm'] = types.ModuleType('aiogram.fsm')
fsm_context = types.ModuleType('aiogram.fsm.context')
fsm_context.FSMContext = object
sys.modules['aiogram.fsm.context'] = fsm_context
fsm_state = types.ModuleType('aiogram.fsm.state')
fsm_state.State = object
fsm_state.StatesGroup = object
sys.modules['aiogram.fsm.state'] = fsm_state

types_mod = types.ModuleType('aiogram.types')
types_mod.Message = object
types_mod.CallbackQuery = object
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

from bot.handlers import profile

# Patch get_connection to raise an error
async def fail_get_connection():
    raise RuntimeError('db broken')

profile.get_connection = fail_get_connection

class DummyState:
    def __init__(self):
        self.data = {
            'telegram_id': 1,
            'username': 'u',
            'bike_type': 'road',
            'skill_level': 'beginner',
            'bio': 'bio'
        }
        self.cleared = False
    async def get_data(self):
        return self.data
    async def clear(self):
        self.cleared = True

class DummyMsg:
    def __init__(self):
        self.text = None
    async def answer(self, text):
        self.text = text
    async def edit_text(self, text):
        self.edit = text

class DummyUser:
    username = 'user'
    full_name = 'User'

class DummyCallback:
    def __init__(self):
        self.data = 'telegram'
        self.from_user = DummyUser()
        self.message = DummyMsg()


def test_handle_contacts_error_message_contains_exception():
    callback = DummyCallback()
    state = DummyState()
    asyncio.run(profile.handle_contacts(callback, state))
    assert 'db broken' in callback.message.text
    assert state.cleared
