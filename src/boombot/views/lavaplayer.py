import hikari
import lavaplayer
import miru

from boombot.embeds.lavaplayer import *

class ResumeButton(miru.Button):
    def __init__(self,
                 lavalink: lavaplayer.LavalinkClient,
                 track: lavaplayer.Track,
                 user: hikari.User) -> None:
        self.lavalink = lavalink
        self.track = track
        self.user = user

        super().__init__(label="Resume", style=hikari.ButtonStyle.SUCCESS)

    async def callback(self, ctx: miru.ViewContext) -> None:
        await self.lavalink.pause(ctx.guild_id, False) 

        await ctx.edit_response(
                embed=PlayerEmbed(self.track, 
                                  self.user,
                                  last_action=f"Player resumed by {ctx.user.username}"))

        self.view.toggle_pause()

class PauseButton(miru.Button):
    def __init__(self,
                 lavalink: lavaplayer.LavalinkClient,
                 track: lavaplayer.Track,
                 user: hikari.User) -> None:
        self.lavalink = lavalink
        self.track = track
        self.user = user

        super().__init__(label="Pause", style=hikari.ButtonStyle.SUCCESS)

    async def callback(self, ctx: miru.ViewContext) -> None:
        await self.lavalink.pause(ctx.guild_id, True) 

        await ctx.edit_response(
                embed=PlayerEmbed(self.track, 
                                  self.user,
                                  last_action=f"Player paused by {ctx.user.username}"))

        self.view.toggle_pause()




class PlayerView(miru.View):
    def __init__(self, 
                 lavalink: lavaplayer.LavalinkClient, 
                 track: lavaplayer.Track, 
                 user: hikari.User, 
                 paused: bool = False,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.play_resume = PauseButton(lavalink, track, user)

        self.add_item(self.play_resume)

    def toggle_pause(self) -> None:
        tmp = None
        if isinstance(self.play_resume, PauseButton):
            tmp = ResumeButton(self.play_resume.lavalink,
                               self.play_resume.track,
                               self.play_resume.user)
        else:
            tmp = PauseButton(self.play_resume.lavalink,
                              self.play_resume.track,
                              self.play_resume.user)

        self.remove_item(self.play_resume)
        self.play_resume = tmp
        self.add_item(self.play_resume)

