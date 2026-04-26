import os
import re
import asyncio
import httpx 
import orjson
import aiofiles
from selectolax.parser import HTMLParser 
from dataclasses import dataclass
from typing import Optional
from Spy import app, logger
from urllib.parse import quote_plus

# Pre-compiled Patterns
TG_LINK_PATTERN = re.compile(r"https?://t\.me/(?:c/)?([^/]+)/(\d+)")
YT_ID_PATTERN = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")

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
        self.limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
        self.client = httpx.AsyncClient(
            http2=True, 
            limits=self.limits,
            timeout=httpx.Timeout(20.0, connect=5.0),
            headers={
                "X-API-Key": self.api_key, 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        )
        os.makedirs("downloads", exist_ok=True)

    async def search_youtube(self, query: str) -> Optional[str]:
        """Direct YouTube search karke video ID nikalne ke liye (Ultra Fast)"""
        # Agar query pehle se hi link hai toh ID extract karo
        match = YT_ID_PATTERN.search(query)
        if match:
            return match.group(1)

        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        try:
            resp = await self.client.get(search_url)
            if resp.status_code != 200:
                return None
            
            # YouTube ke HTML mein 'ytInitialData' variable hota hai jisme saara search result hota hai
            html = resp.text
            start_str = 'var ytInitialData = '
            end_str = ';</script>'
            
            start_idx = html.find(start_str)
            if start_idx == -1:
                return None
            
            start_idx += len(start_str)
            end_idx = html.find(end_str, start_idx)
            json_str = html[start_idx:end_idx].strip()
            
            # data parse karein
            data = orjson.loads(json_str)
            
            # Video ID nikalne ka deep path
            contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
            
            for section in contents:
                if "itemSectionRenderer" in section:
                    for item in section["itemSectionRenderer"]["contents"]:
                        if "videoRenderer" in item:
                            return item["videoRenderer"]["videoId"]
        except Exception as e:
            logger.error(f"YouTube Search Error: {e}")
        return None

    async def get_track(self, url: str) -> Optional[MusicTrack]:
        endpoint = f"{self.api_url}/api/track"
        params = {"url": url}
        try:
            resp = await self.client.get(endpoint, params=params)
            if resp.status_code == 200:
                data = orjson.loads(resp.content)
                return MusicTrack(
                    cdnurl=data.get("cdnurl", ""),
                    url=data.get("url", ""),
                    id=data.get("id", ""),
                    key=data.get("key")
                )
        except Exception as e:
            logger.error(f"Fetch Error: {e}")
        return None

    async def download_track(self, query: str) -> Optional[str]:
        """Ab ye query (song name) ya URL dono handle karega"""
        # 1. YouTube se Video ID dhundo
        video_id = await self.search_youtube(query)
        if not video_id:
            logger.error("Video not found on YouTube.")
            return None

        yt_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # 2. API se download link lo
        track = await self.get_track(yt_url)
        if not track or not track.cdnurl:
            return None

        # 3. Telegram Link Check
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

        # 4. Direct Fast Download
        save_path = f"downloads/{video_id}.mp3"
        try:
            async with self.client.stream("GET", track.cdnurl) as response:
                if response.status_code != 200:
                    return None
                
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=1024*1024):
                        await f.write(chunk)
            return save_path
        except Exception as e:
            logger.error(f"Download Fail: {e}")
            return None

    async def close(self):
        await self.client.aclose()
