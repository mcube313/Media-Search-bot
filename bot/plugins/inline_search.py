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


from pyrogram.types import (
    InlineQuery
)
from pyrogram.errors import (
    QueryIdInvalid
)
from bot.bot import Bot
from bot.helper_functions.telegram_user_search import (
    search_tg
)


@Bot.on_inline_query()
async def recvd_iq(client: Bot, inline_query: InlineQuery):
    start_at = int(inline_query.offset or 0)
    limit = 9
    new_offset = start_at + limit
    search_query = inline_query.query
    # LOGGER(__name__).info(search_query)
    search_results = []
    switch_pm_text_s = ""
    if search_query.strip() != "":
        search_results, tryt = await search_tg(
            client.USER,
            client,
            search_query,
            start_at,
            1
        )
        len_srch_ress = len(search_results)
        switch_pm_text_s = (
            f"Found {len_srch_ress} / {tryt} "
            f"results for {search_query}"
        )
    else:
        switch_pm_text_s = (
            "Enter a Name to Search"
        )
    if len(search_results) == 0:
        new_offset = ""
    new_offset = str(new_offset)
    try:
        await inline_query.answer(
            results=search_results,
            cache_time=9990999,
            switch_pm_text=switch_pm_text_s,
            switch_pm_parameter="inline",
            next_offset=new_offset
        )
    except QueryIdInvalid:
        pass
