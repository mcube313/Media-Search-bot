#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  https://github.com/SpEcHiDe/Media-Search-bot
#  Copyright (C) 2021 Shrimadhav U K

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from dotenv import load_dotenv


# apparently, no error appears even if the path does not exists
load_dotenv("config.env")


class Config:
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", None)
    # Get these values from my.telegram.org
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", None)
    TG_USER_SESSION = os.environ.get("TG_USER_SESSION", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    #
    TG_UPDATE_WORKERS_COUNT = int(os.environ.get("TG_UPDATE_WORKERS_COUNT", 1))
    TG_DUMP_CHAT = int(os.environ.get("TG_DUMP_CHAT", "-100"))
    # strings
    START_TEXT = os.environ.get("START_TEXT", "/start")
    PLZ_RATE_TEXT = os.environ.get("PLZ_RATE_TEXT", "/rate")
    # tg search helpers
    DL_START_GAT = os.environ.get("DL_START_GAT", "id")
    SRCH_START_GAT = os.environ.get("SRCH_START_GAT", "#ID")
    US_SEPERAT_OR = os.environ.get("US_SEPERAT_OR", "_")


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
