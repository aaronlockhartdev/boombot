import os
import time

from dotenv import load_dotenv

def main() -> None:
    print(f"""
    ___       ___       ___       ___            ___       ___       ___   
   /\  \     /\  \     /\  \     /\__\          /\  \     /\  \     /\  \  
  /::\  \   /::\  \   /::\  \   /::L_L_        /::\  \   /::\  \    \:\  \ 
 /::\:\__\ /:/\:\__\ /:/\:\__\ /:/L:\__\      /::\:\__\ /:/\:\__\   /::\__\ 
 \:\::/  / \:\/:/  / \:\/:/  / \/_/:/  /      \:\::/  / \:\/:/  /  /:/\/__/
  \::/  /   \::/  /   \::/  /    /:/  /        \::/  /   \::/  /   \/__/   
   \/__/     \/__/     \/__/     \/__/          \/__/     \/__/            
Running BoomBot...
          """)

    load_dotenv()

    env_vars = {
            'DISCORD_TOKEN',
            'LAVALINK_IP',
            'LAVALINK_PORT',
            'LAVALINK_PASSWORD',
            }

    if not env_vars.issubset(os.environ.keys()):
        raise Exception("Missing essential environmental variables for configuration")


    import boombot
    boombot.run()

if __name__ == '__main__':
    main()
