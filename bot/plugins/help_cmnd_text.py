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


from pyrogram import (
    filters
)
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bot import (
    DL_START_GAT,
    PLZ_RATE_TEXT,
    SRCH_START_GAT,
    START_TEXT,
    TG_DUMP_CHAT_S,
    US_SEPERAT_OR
)
from bot.bot import Bot
from bot.helper_functions.one_id_gett_er import (
    get_uid
)
from bot.helper_functions.get_file_types import (
    get_file_id
)


@Bot.on_message(
    filters.command("start")
)
async def start_m_comnd(client: Bot, message: Message):
    if len(message.command) > 1:
        fake_id = message.command[1].lower()
        if not fake_id.startswith(f"{DL_START_GAT}{US_SEPERAT_OR}"):
            await message.delete()
            return
        _, fake_id = fake_id.split(US_SEPERAT_OR)
        fake_id = int(fake_id)
        current_srch_indix = 1
        real_m_media = await get_uid(
            client.USER,
            current_srch_indix,
            fake_id
        )
        if not real_m_media:
            await message.delete()
            return
        real_message = await client.get_messages(
            chat_id=TG_DUMP_CHAT_S[current_srch_indix],
            message_ids=real_m_media.file_id,
            replies=1
        )
        __dummy_text = real_message.caption or ""
        if (
            f"{SRCH_START_GAT}{US_SEPERAT_OR}" in __dummy_text and
            real_m_media.caption and
            f"{SRCH_START_GAT}{US_SEPERAT_OR}" not in real_m_media.caption
        ):
            __dummy_text = real_m_media.caption
        elif (
            f"{SRCH_START_GAT}{US_SEPERAT_OR}" in __dummy_text
        ):
            __dummy_text = " "
        tg_media = get_file_id(real_message)
        await message.reply_cached_media(
            file_id=tg_media.file_id,
            quote=True,
            caption=__dummy_text,
            disable_notification=True,
            reply_to_message_id=message.message_id
        )
    else:
        share_text = (
            "https%3A%2F%2Fgithub.com%2FSpEcHiDe%2FMedia-Search-bot"
        )
        share_url = (
            "https://t.me"
            f"/share/url?url={share_text}"
        )
        await message.reply_text(
            START_TEXT,
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text="Find a Telegram File",
                    switch_inline_query_current_chat=""
                ), InlineKeyboardButton(
                    text="Find & Share Files with Friends",
                    switch_inline_query=""
                )], [InlineKeyboardButton(
                    text="Share this Bot with your friends",
                    url=share_url
                )]
            ])
        )


@Bot.on_message(
    filters.command("rate")
)
async def rate_cmnd(_, message: Message):
    await message.reply_text(
        PLZ_RATE_TEXT,
        quote=True,
        disable_web_page_preview=True
    )
