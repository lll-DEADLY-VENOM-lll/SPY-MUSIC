from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER

class Sagar(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="Spy",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # LOGGER_ID ko integer mein convert karne ki koshish (ValueError se bachne ke liye)
        try:
            if config.LOGGER_ID:
                log_id = int(config.LOGGER_ID)
            else:
                LOGGER(__name__).error("LOGGER_ID config file mein nahi mila.")
                exit()
        except ValueError:
            LOGGER(__name__).error("LOGGER_ID galat hai! Ye sirf numbers (integer) hona chahiye aur -100 se shuru hona chahiye.")
            exit()

        try:
            await self.send_message(
                chat_id=log_id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot log group tak nahi pahunch pa raha. Check karein ki aapne Bot ko Log Group mein add kiya hai ya nahi."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        # Check Admin Status
        try:
            a = await self.get_chat_member(log_id, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Bot ko Log Group mein ADMIN banayein!"
                )
                exit()
        except Exception as e:
            LOGGER(__name__).error(f"Admin status check karne mein galti: {e}")
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot stopped.")
