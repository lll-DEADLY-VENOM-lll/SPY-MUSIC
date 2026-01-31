from pyrogram import Client
import config
from ..logging import LOGGER

# Global lists for tracking assistants
assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = None
        self.two = None
        self.three = None
        self.four = None
        self.five = None
        
        # Session strings ki list config se
        self.sessions = [
            (config.STRING1, "one", "DilXAss1"),
            (config.STRING2, "two", "DilXAss2"),
            (config.STRING3, "three", "DilXAss3"),
            (config.STRING4, "four", "DilXAss4"),
            (config.STRING5, "five", "DilXAss5"),
        ]

        # Clients initialize karna
        for string, attr, name in self.sessions:
            if string:
                client = Client(
                    name=name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(string),
                    no_updates=True,
                )
                setattr(self, attr, client)

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        
        # Ek loop jo check karega self.one se self.five tak jo bhi active hai
        for i, (string, attr, _) in enumerate(self.sessions, start=1):
            client = getattr(self, attr)
            
            if client:
                try:
                    await client.start()
                    
                    # Support Group Join Karna
                    try:
                        await client.join_chat("about_deadly_venom")
                    except:
                        pass

                    # Log Group mein message bhejna
                    try:
                        await client.send_message(config.LOGGER_ID, f"Assistant {i} Started")
                    except:
                        LOGGER(__name__).error(
                            f"Assistant Account {i} log group access nahi kar pa raha. "
                            f"Check karein ki assistant admin hai ya nahi!"
                        )
                        exit()

                    # Data set karna
                    me = await client.get_me()
                    client.id = me.id
                    client.name = me.mention
                    client.username = me.username
                    
                    # Global lists update karna
                    assistants.append(i)
                    assistantids.append(me.id)
                    
                    LOGGER(__name__).info(f"Assistant {i} Started as {client.name}")
                    
                except Exception as e:
                    LOGGER(__name__).error(f"Assistant {i} fail ho gaya start hone mein: {str(e)}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        # Saare active clients ko loop karke stop karna
        for _, attr, _ in self.sessions:
            client = getattr(self, attr)
            if client:
                try:
                    await client.stop()
                except:
                    pass

# Made with ❤️ for your Userbot
