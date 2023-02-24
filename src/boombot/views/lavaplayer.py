import logging

import hikari
import lavaplayer
import miru

from boombot.embeds.lavaplayer import *

class PauseResumeButton(miru.Button):
    def __init__(self,
                 lavalink: lavaplayer.LavalinkClient,
                 track: lavaplayer.Track,
                 user: hikari.User,
                 *args, **kwargs) -> None:
        self.lavalink = lavalink
        self.track = track
        self.user = user

        super().__init__(label="Pause", style=hikari.ButtonStyle.SECONDARY, *args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        pause = self.label == "Pause"

        await self.lavalink.pause(ctx.guild_id, pause)
        
        self.label="Resume" if pause else "Pause"
        self.style=hikari.ButtonStyle.SUCCESS if pause else hikari.ButtonStyle.SECONDARY

        await ctx.edit_response(
                embed=PlayerEmbed(self.track,
                                 self.user,
                                 last_action=f"Player {'paused' if pause else 'resumed'} by {ctx.user.username} ♪"),
                components=self.view)
        

class SkipButton(miru.Button):
    def __init__(self,
                 lavalink: lavaplayer.LavalinkClient,
                 track: lavaplayer.Track,
                 user: hikari.User,
                 *args, **kwargs) -> None:
        self.lavalink = lavalink
        self.track = track
        self.user = user

        super().__init__(label="Skip", style=hikari.ButtonStyle.SECONDARY, *args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        await self.lavalink.skip(ctx.guild_id)
        await ctx.edit_response(
                embed=PlayerEmbed(self.track,
                                 self.user,
                                 last_action=f"Player skipped by {ctx.user.username} ♪"),
        )


class PlayerView(miru.View):
    def __init__(self, 
                 lavalink: lavaplayer.LavalinkClient, 
                 track: lavaplayer.Track, 
                 user: hikari.User, 
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(PauseResumeButton(lavalink, track, user))
        self.add_item(SkipButton(lavalink, track, user))
