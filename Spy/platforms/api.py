import os
import re
import httpx 
import orjson
import aiofiles
from dataclasses import dataclass
from typing import Optional
from kiru import app, logger

# YouTube.py se Scraper import karein
from YouTube import YouTubeAPI 

TG_LINK_PATTERN = re.compile(r"https?://t\.me/(?:c/)?([^/]+)/(\d+)")

@dataclass(slots=True)
class MusicTrack:
    cdnurl: str
    url: str
    id: str
    key: Optional[str] = None

class FallenApi:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            http2=True, 
            timeout=httpx.Timeout(20.0, connect=5.0),
            headers={
                "X-API-Key": self.api_key, 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
        )
        # YouTube Scraper ko initialize kiya
        self.yt = YouTubeScraper(self.client)
        os.makedirs("downloads", exist_ok=True)

    async def get_track(self, url: str) -> Optional[MusicTrack]:
        endpoint = f"{self.api_url}/api/track"
        try:
            resp = await self.client.get(endpoint, params={"url": url})
            if resp.status_code == 200:
                data = orjson.loads(resp.content)
                return MusicTrack(
                    cdnurl=data.get("cdnurl", ""),
                    url=data.get("url", ""),
                    id=data.get("id", ""),
                    key=data.get("key")
                )
        except Exception as e:
            logger.error(f"API Error: {e}")
        return None

    async def download_track(self, query: str) -> Optional[str]:
        # 1. YouTube.py ka use karke ID nikalna
        video_id = await self.yt.get_video_id(query)
        if not video_id:
            logger.error("Video not found.")
            return None

        yt_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # 2. Fallen API se track info lena
        track = await self.get_track(yt_url)
        if not track or not track.cdnurl:
            return None

        # 3. Telegram Download logic
        tg_match = TG_LINK_PATTERN.match(track.cdnurl)
        if tg_match:
            try:
                chat_id = tg_match.group(1)
                msg_id = int(tg_match.group(2))
                if chat_id.isdigit(): chat_id = int(f"-100{chat_id}")
                msg = await app.get_messages(chat_id, msg_id)
                if msg:
                    return await msg.download(file_name=f"downloads/{video_id}.mp3")
            except Exception as e:
                logger.error(f"TG Error: {e}")

        # 4. Fast HTTP Stream Download
        save_path = f"downloads/{video_id}.mp3"
        try:
            async with self.client.stream("GET", track.cdnurl) as resp:
                if resp.status_code == 200:
                    async with aiofiles.open(save_path, "wb") as f:
                        async for chunk in resp.aiter_bytes(chunk_size=1024*1024):
                            await f.write(chunk)
                    return save_path
        except Exception as e:
            logger.error(f"Download Fail: {e}")
        return None

    async def close(self):
        await self.client.aclose()
