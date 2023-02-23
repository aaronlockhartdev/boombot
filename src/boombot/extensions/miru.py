import logging

import hikari
import lightbulb
import miru

logging.info("Loading miru plugin")

plugin = lightbulb.Plugin("miru")

def load(bot):
    miru.install(bot)

    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
