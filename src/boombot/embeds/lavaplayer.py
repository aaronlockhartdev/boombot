import re

import hikari
import lavaplayer

class PlayerEmbed(hikari.Embed):
    def __init__(self, 
                 track: lavaplayer.Track,
                 user: hikari.User, 
                 last_action: str = None) -> None:

        h, m = divmod(track.length//1000, 3600)
        m, s = divmod(m, 60)
        track_time = "%d:%02d" % (m, s) if not h else "%d:%02d:%02d" % (h, m, s)

        yt_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", track.uri).group(1)
        thumbnail = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"

        avatar = user.avatar_url if user.avatar_url else user.default_avatar_url

        description=f"[{track.title}]({track.uri})\n`[0:00/{track_time}]`"

        if last_action: description += "\n\n" + last_action

        super().__init__(
                title="Now Playing ♫",
                description=description)

        self.set_thumbnail(thumbnail) \
        .set_footer(
                text=f"Played by {user.username}",
                icon=avatar)

