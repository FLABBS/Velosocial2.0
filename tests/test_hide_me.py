import sys
import types
import sqlite3
import asyncio

# Stub aiogram modules similar to other tests
aiogram = types.ModuleType("aiogram")
class DummyRouter:
    def message(self, *a, **k):
        def decorator(f):
            return f
        return decorator
    def errors(self, *a, **k):
        def decorator(f):
            return f
        return decorator
aiogram.Router = DummyRouter
class DummyF:
    def __init__(self):
        self.data = types.SimpleNamespace()
        self.location = object()
        self.text = object()
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
sys.modules['aiogram.fsm.context'] = types.ModuleType('aiogram.fsm.context')
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
exceptions_mod = types.ModuleType('aiogram.exceptions')
exceptions_mod.TelegramAPIError = Exception
sys.modules['aiogram.exceptions'] = exceptions_mod

# Stub aiosqlite so database module loads
aiosqlite_mod = types.ModuleType('aiosqlite')
class DummyConn:
    pass
aiosqlite_mod.Connection = DummyConn
sys.modules['aiosqlite'] = aiosqlite_mod

from bot.handlers import common

# Create in-memory sqlite DB and patch connection
class FakeConn:
    def __init__(self, real):
        self.real = real
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass
    async def execute(self, *a):
        self.real.execute(*a)
    async def commit(self):
        self.real.commit()

db = sqlite3.connect(':memory:')
db.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT,
    bike_type TEXT,
    skill_level TEXT,
    bio TEXT,
    contacts TEXT,
    lat REAL,
    lon REAL,
    is_visible BOOLEAN DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
db.execute("INSERT INTO users (telegram_id, username, is_visible) VALUES (1, 'u', 1)")
db.commit()

async def fake_get_connection():
    return FakeConn(db)

common.get_connection = fake_get_connection

class DummyUser:
    id = 1

class DummyMessage:
    def __init__(self):
        self.from_user = DummyUser()
        self.text = None
    async def answer(self, text):
        self.text = text


def test_hide_me_updates_visibility():
    msg = DummyMessage()
    asyncio.run(common.cmd_hide_me(msg))
    cur = db.cursor()
    cur.execute('SELECT is_visible FROM users WHERE telegram_id = 1')
    assert cur.fetchone()[0] == 0
    assert "скрыты" in msg.text
