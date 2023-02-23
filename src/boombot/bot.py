import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os
import logging

import hikari
import lightbulb

bot = lightbulb.BotApp(
    os.getenv('DISCORD_TOKEN'),
    intents=hikari.Intents.ALL_GUILDS_UNPRIVILEGED,
    banner=None,
    logs="INFO"
)

@bot.listen()
async def load_extensions(_: hikari.StartedEvent) -> None:
    bot.load_extensions("boombot.extensions.lavaplayer")
    bot.load_extensions("boombot.extensions.miru")

@bot.command()
@lightbulb.command("ping", description="Latency test.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    logging.info("Ping received.")
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency * 1000:.2f}ms.")
