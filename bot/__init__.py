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


""" init """

# the logging things
import logging
from logging.handlers import RotatingFileHandler
# the secret configuration specific things
from bot.sample_config import Config

# path to store LOG files
LOG_FILE_ZZGEVC = "MediaSearchBot.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC,
            maxBytes=20480,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)


# TODO: is there a better way?
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
TG_BOT_TOKEN = Config.TG_BOT_TOKEN
TG_USER_SESSION = Config.TG_USER_SESSION
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
TG_UPDATE_WORKERS_COUNT = Config.TG_UPDATE_WORKERS_COUNT

TG_DUMP_CHAT_S = [
    Config.TG_DUMP_CHAT
]

PLZ_RATE_TEXT = Config.PLZ_RATE_TEXT
START_TEXT = Config.START_TEXT

DL_START_GAT = Config.DL_START_GAT
SRCH_START_GAT = Config.SRCH_START_GAT
US_SEPERAT_OR = Config.US_SEPERAT_OR
