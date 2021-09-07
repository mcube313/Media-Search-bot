#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from telethon import (
    TelegramClient,
    events,
    Button
)
from telethon.sessions import StringSession
from telethon.errors import (
    QueryIdInvalidError
)
from get_config import get_config

# apparently, no error appears even if the path does not exists
load_dotenv("config.env")

# The Telegram API things
# Get these values from my.telegram.org or Telegram: @useTGxBot
API_HASH = get_config("API_HASH", should_prompt=True)
APP_ID = int(get_config("APP_ID", should_prompt=True))
# get a token from @BotFather
TG_BOT_TOKEN = get_config("TG_BOT_TOKEN", should_prompt=True)
# yet another, privacy respecting DustBin Chat
TG_DB_CHAT = int(get_config("TG_DB_CHAT"))
# generate a StringSession for the user account
TG_USER_SESSION = get_config("TG_USER_SESSION", should_prompt=True)

# hack :\
TG_BOT_ID = int(TG_BOT_TOKEN.split(":")[0])


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "GetSongsBot.log",
            maxBytes=50000000,
            backupCount=1
        ),
        logging.StreamHandler()
    ]
)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)


client = TelegramClient(
    "MediaSearchBot",
    APP_ID,
    API_HASH
).start(bot_token=TG_BOT_TOKEN)
client.parse_mode = "html"

user_client = TelegramClient(
    StringSession(TG_USER_SESSION),
    APP_ID,
    API_HASH
).start()
user_client.parse_mode = "html"


async def search_tg(
    _u: TelegramClient,
    _b: TelegramClient,
    event: events.InlineQuery.Event,
    sqr: str,
    astr: int,
    lmtn: int
):
    mtls = await _u.get_messages(
        entity=TG_DB_CHAT,
        limit=lmtn,
        offset_id=astr,
        search=sqr
    )
    t_r = mtls.total
    builder = event.builder
    search_results = []
    for mt_ls in mtls:
        sltm = await _b.get_messages(
            entity=TG_DB_CHAT,
            ids=mt_ls.id
        )
        if sltm:
            title = sltm.file.name or " "
            description = sltm.raw_text or " "
            search_results.append(builder.document(
                file=sltm.media,
                title=title,
                description=description,
                text=sltm.text,
                buttons=[Button.switch_inline(
                    text="Search Again",
                    query=sqr,
                    same_peer=True
                )]
            ))
    return search_results, t_r


@client.on(events.InlineQuery)
async def handler(event: events.InlineQuery.Event):
    # LOGGER(__name__).info(event.stringify())
    start_at = int(event.offset or 0)
    limit = 9
    new_offset = str(start_at + limit)
    search_query = event.query.query
    search_results = []
    switch_pm_text_s = ""
    if search_query.strip() != "":
        search_results, tr_ = await search_tg(
            user_client,
            client,
            event,
            search_query,
            start_at,
            limit
        )
        len_srch_ress = len(search_results)
        switch_pm_text_s = (
            f"Found {len_srch_ress} / {tr_} "
            f"results for {search_query}"
        )
    else:
        switch_pm_text_s = (
            "Enter something to Search"
        )
    if len(search_results) < limit:
        new_offset = None
    try:
        await event.answer(
            results=search_results,
            cache_time=300,
            gallery=False,
            next_offset=new_offset,
            private=False,
            switch_pm=switch_pm_text_s,
            switch_pm_param="inline"
        )
    except QueryIdInvalidError:
        await event.answer(
            results=[],
            cache_time=300,
            gallery=False,
            next_offset=None,
            private=False,
            switch_pm="please /start bot first 😞😞",
            switch_pm_param="toolongxtion"
        )


@client.on(events.NewMessage)
async def _(evt: events.NewMessage.Event):
    if evt.via_bot_id and evt.via_bot_id == TG_BOT_ID:
        return

    if not evt.is_private:
        return

    if evt.file:
        return

    await evt.reply(
        "Help To Find Files",
        file="CAACAgUAAxkBAAEBWs9hN7s2Vl_7Ta0Faoau9Y9_N5WwkQACMAQAAkO5sVXoQIxpJHXYZh4E",
        buttons=[
            [
                Button.switch_inline(
                    text="Search in this Chat",
                    query="",
                    same_peer=True
                ),
                Button.switch_inline(
                    text="Search in Another Chat",
                    query="",
                    same_peer=False
                )
            ],
            [
                Button.url(
                    text="✅ I agree to the TnC",
                    url="https://t.me/mcubemediaofficial"
                )
            ]
        ]
    )


LOGGER(__name__).info("Started")
client.run_until_disconnected()
