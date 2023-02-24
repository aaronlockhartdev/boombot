import hikari

class InfoEmbed(hikari.Embed):
    def __init__(self, 
                 title: str, 
                 msg: str, 
                 *args, 
                 **kwargs) -> None:
        super().__init__(title=title, 
                         description=msg, 
                         color=hikari.Color(0xeb0c8a), 
                         *args, **kwargs)

        #self.set_thumbnail()

class ErrorEmbed(hikari.Embed):
    def __init__(self, error: str, *args, **kwargs) -> None:
        super().__init__(title="Error",
                         description=error,
                         color=hikari.Color(0xff0000),
                         *args, **kwargs)
