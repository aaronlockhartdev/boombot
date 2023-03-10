import os
import re
import time
import logging
import asyncio

import hikari
import lightbulb
import lavaplayer

from boombot.embeds.general import *

from boombot.views.lavaplayer import *
from boombot.embeds.lavaplayer import *

logging.info("Loading lavaplayer plugin")

plugin = lightbulb.Plugin("lavaplayer")

lavalink = lavaplayer.LavalinkClient(
        host=os.getenv('LAVALINK_HOST'),
        port=int(os.getenv('LAVALINK_PORT')),
        password=os.getenv('LAVALINK_PASSWORD')
        )

# On voice state update the bot will update the lavalink node
@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent):
    await lavalink.raw_voice_state_update(event.guild_id, event.state.user_id, event.state.session_id, event.state.channel_id)

@plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent):
    await lavalink.raw_voice_server_update(event.guild_id, event.endpoint, event.token)    

# Commands
# ------------------------------------- #
@plugin.command()
@lightbulb.command(name="join", description="join voice channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def join_command(ctx: lightbulb.context.Context):
    voice_state = ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state: 
        await ctx.respond("you are not in a voice channel")
        return

    channel_id = voice_state.channel_id
    await plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    await lavalink.wait_for_connection(ctx.guild_id)
    await ctx.respond(embed=InfoEmbed(
        f"Boom bot has joined <#{channel_id}>!",
        f"Nice to meetcha!"))

@plugin.command()
@lightbulb.option(name="query", description="query to search", required=True)
@lightbulb.command(name="play", description="Play command", aliases=["p"])
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(ctx: lightbulb.context.Context):
    if not await lavalink.get_guild_node(ctx.guild_id): await join_command(ctx)

    query = ctx.options.query
    result = await lavalink.auto_search_tracks(query)
    if not result:
        await ctx.respond("not found result for your query")
    elif isinstance(result, lavaplayer.TrackLoadFailed):
        await ctx.respond("Track load failed, try again later.\n```{}```".format(result.message))
    elif isinstance(result, lavaplayer.PlayList):
        await lavalink.add_to_queue(ctx.guild_id, result.tracks, ctx.author.id)
        await ctx.respond(f"added {len(result.tracks)} tracks to queue")
    else:
        track = result[0]
        await lavalink.add_to_queue(ctx.guild_id, [track], ctx.author.id)  # play the first result

        view = PlayerView(lavalink, track, ctx.user)

        msg = await ctx.respond(
                embed=PlayerEmbed(track, ctx.user),
                components=view
                )

        await view.start(msg)


@plugin.command()
@lightbulb.command(name="stop", description="Stop command", aliases=["s"])
@lightbulb.implements(lightbulb.SlashCommand)
async def stop_command(ctx: lightbulb.context.Context):
    await lavalink.stop(ctx.guild_id)
    await ctx.respond(embed=InfoEmbed(
        title="Music Stopped ???",
        msg=f"Music stopped by {ctx.user.username} ???"))


@plugin.command()
@lightbulb.command(name="pause", description="Pause command")
@lightbulb.implements(lightbulb.SlashCommand)
async def pause_command(ctx: lightbulb.context.Context):
    await lavalink.pause(ctx.guild_id, True)
    await ctx.respond(embed=InfoEmbed(
        title="Music Paused ???",
        msg=f"Music paused by {ctx.user.username} ???"))

@plugin.command()
@lightbulb.command(name="resume", description="Resume command")
@lightbulb.implements(lightbulb.SlashCommand)
async def resume_command(ctx: lightbulb.context.Context):
    await lavalink.pause(ctx.guild_id, False)
    await ctx.respond(embed=InfoEmbed(
        title="Music Resumed ???",
        msg=f"Music paused by {ctx.user.username} ???"))

@plugin.command()
@lightbulb.command(name="queue", description="Queue command")
@lightbulb.implements(lightbulb.SlashCommand)
async def queue_command(ctx: lightbulb.context.Context):
    node = await lavalink.get_guild_node(ctx.guild_id)
    await ctx.respond(embed=InfoEmbed(
        title="Music Queue ???",
        msg="\n".join([f"{n+1}. [{i.title}]({i.uri})" for n, i in enumerate(node.queue)])))

@plugin.command()
@lightbulb.command(name="np", description="Now playing command")
@lightbulb.implements(lightbulb.SlashCommand)
async def np_command(ctx: lightbulb.context.Context):
    node = await lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.queue:
        await ctx.respond("nothing playing")
        return
    await ctx.respond(f"[{node.queue[0].title}]({node.queue[0].uri})")

@plugin.command()
@lightbulb.command(name="repeat", description="Repeat command")
@lightbulb.implements(lightbulb.SlashCommand)
async def repeat_command(ctx: lightbulb.context.Context):
    node = await lavalink.get_guild_node(ctx.guild_id)
    stats = False if node.repeat else True
    await lavalink.repeat(ctx.guild_id, stats)
    if stats:
        await ctx.respond("done repeat the music")
        return
    await ctx.respond("done stop repeat the music")

@plugin.command()
@lightbulb.command(name="shuffle", description="Shuffle command")
@lightbulb.implements(lightbulb.SlashCommand)
async def shuffle_command(ctx: lightbulb.context.Context):
    await lavalink.shuffle(ctx.guild_id)
    await ctx.respond("done shuffle the music")

@plugin.command()
@lightbulb.command(name="leave", description="Leave command")
@lightbulb.implements(lightbulb.SlashCommand)
async def leave_command(ctx: lightbulb.context.Context):
    await plugin.bot.update_voice_state(ctx.guild_id, None)
    await ctx.respond(embed=InfoEmbed(
        f"Boom bot has left the channel",
        f"Bye bye!"))

# ------------------------------------- #

@lavalink.listen(lavaplayer.TrackStartEvent)
async def track_start_event(event: lavaplayer.TrackStartEvent):
    logging.info(f"start track: {event.track.title}")

@lavalink.listen(lavaplayer.TrackEndEvent)
async def track_end_event(event: lavaplayer.TrackEndEvent):
    logging.info(f"track end: {event.track.title}")

@lavalink.listen(lavaplayer.WebSocketClosedEvent)
async def web_socket_closed_event(event: lavaplayer.WebSocketClosedEvent):
    logging.error(f"error with websocket {event.reason}")

# ------------------------------------- #

def load(bot):
    lavalink.set_user_id(bot.get_me().id)
    lavalink.set_event_loop(asyncio.get_event_loop())
    lavalink.connect()

    bot.add_plugin(plugin)
def unload(bot):
    bot.remove_plugin(plugin)


