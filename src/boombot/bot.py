# install uvloop
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os
import logging

import hikari
import lightbulb

from hikari import Intents

INTENTS = Intents.ALL_GUILDS_UNPRIVILEGED

bot = lightbulb.BotApp(
    os.getenv('DISCORD_TOKEN'),
    intents=INTENTS,
    banner=None,
    logs="INFO"
)

@bot.listen()
async def starting_load_extensions(_: hikari.StartingEvent) -> None:
    """Load the music extension when Bot starts."""
    bot.load_extensions("boombot.extensions.lavasnek")

@bot.command()
@lightbulb.command("ping", description="Latency test.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    logging.info("Ping received.")
    await ctx.respond(f"Boing! Latency: {bot.heartbeat_latency * 1000:.2f}ms.")
