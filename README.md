# Velosocial Bot

Velosocial is a Telegram bot that helps cyclists find each other, share locations
and organise group rides. The project is built with [aiogram](https://github.com/aiogram/aiogram)
and uses SQLite for persistence.

## Installation

1. Clone the repository
   ```bash
   git clone <repo_url>
   cd Velosocial2.0
   ```
2. Create a Python 3.11 virtual environment and install the dependencies
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Environment setup

The bot reads configuration from environment variables. You can create a `.env`
file based on `.env.example` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:

- `TELEGRAM_TOKEN` – token from @BotFather
- `YANDEX_MAPS_API_KEY` – API key for the Yandex Static Maps API
- `YANDEX_GEOCODER_API_KEY` – API key for the Yandex Geocoder API
- `LOG_LEVEL` (optional) – logging level, defaults to `INFO`

### Obtaining API keys

1. **Telegram** – create a new bot via [@BotFather](https://t.me/BotFather) and
   copy the token it gives you.
2. **Yandex** – sign up at <https://developer.tech.yandex.ru/>, create a new
   project and enable the "Static Maps" and "Geocoder" APIs to obtain the
   corresponding keys.

## Running the bot

After installing the dependencies and setting the environment variables, launch
`main.py`:

```bash
python main.py
```

The bot will start polling Telegram for updates.

## Usage

Some basic commands available in the bot:

- `/start` – show welcome message
- `/profile` – create or edit your profile
- `/find` – search for cyclists near you using location or address
- `/create_event` – organise a group ride
- `/help` – show help text

A typical workflow:

1. Send `/profile` and follow the instructions to create a profile.
2. Use `/find` to look for cyclists around you.
3. Run `/create_event` to schedule a ride and automatically create a group chat
   for participants.

Logs are written to `bot.log` as well as the console. Adjust the level with
`LOG_LEVEL` if necessary.
