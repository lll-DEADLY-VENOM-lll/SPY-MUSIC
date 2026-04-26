import os
import re
import asyncio
import httpx
import orjson
import aiofiles
from urllib.parse import quote_plus
from dataclasses import dataclass
from typing import Optional
from kiru import app, logger  # Aapke bot/app ke instances

# --- Configuration & Patterns ---
TG_LINK_PATTERN = re.compile(r"https?://t\.me/(?:c/)?([^/]+)/(\d+)")
YT_LINK_PATTERN = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")

@dataclass(slots=True)
class MusicTrack:
    cdnurl: str
    url: str
    id: str
    key: Optional[str] = None

# --- YouTube Scraping Logic ---
class YouTubeAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.search_url = "https://www.youtube.com/results?search_query="

    async def get_video_url(self, query: str) -> Optional[str]:
        """Gaane ke naam se YouTube URL nikalne ke liye"""
        # Agar input pehle se hi link hai
        if YT_LINK_PATTERN.search(query):
            return query

        try:
            url = f"{self.search_url}{quote_plus(query)}"
            resp = await self.client.get(url)
            if resp.status_code != 200:
                return None

            html = resp.text
            # YouTube ke hidden JSON data ko extract karna (Ultra Fast)
            start_str = 'var ytInitialData = '
            start_idx = html.find(start_str)
            if start_idx == -1: return None
            
            start_idx += len(start_str)
            end_idx = html.find(';</script>', start_idx)
            data = orjson.loads(html[start_idx:end_idx].strip())

            # JSON se pehla Video ID nikalna
            contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
            for section in contents:
                if "itemSectionRenderer" in section:
                    for item in section["itemSectionRenderer"]["contents"]:
                        if "videoRenderer" in item:
                            v_id = item["videoRenderer"]["videoId"]
                            return f"https://www.youtube.com/watch?v={v_id}"
        except Exception as e:
            logger.error(f"YouTube Search Error: {e}")
        return None

# --- Main API Logic ---
class FallenApi:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        # High-performance HTTP/2 Client
        self.client = httpx.AsyncClient(
            http2=True,
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={
                "X-API-Key": self.api_key,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        )
        # YouTube Logic ko connect kiya
        self.yt_api = YouTubeAPI(self.client)
        os.makedirs("downloads", exist_ok=True)

    async def get_track_info(self, yt_url: str) -> Optional[MusicTrack]:
        """Backend API se track ka download link lena"""
        endpoint = f"{self.api_url}/api/track"
        try:
            resp = await self.client.get(endpoint, params={"url": yt_url})
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
        """Main Function: Search -> API -> Download"""
        # 1. YouTube se URL dhoondo
        yt_url = await self.yt_api.get_video_url(query)
        if not yt_url:
            logger.error("Video not found on YouTube.")
            return None

        # 2. Fallen API se CDN Link lo
        track = await self.get_track_info(yt_url)
        if not track or not track.cdnurl:
            logger.error("Failed to get download link from API.")
            return None

        # 3. Agar link Telegram ka hai (Fastest Download)
        tg_match = TG_LINK_PATTERN.match(track.cdnurl)
        if tg_match:
            try:
                chat_id = tg_match.group(1)
                msg_id = int(tg_match.group(2))
                if chat_id.isdigit(): chat_id = int(f"-100{chat_id}")
                
                msg = await app.get_messages(chat_id, msg_id)
                if msg:
                    return await msg.download(file_name=f"downloads/{track.id}.mp3")
            except Exception as e:
                logger.error(f"Telegram Download Error: {e}")

        # 4. Direct HTTP Stream Download (Agar TG link nahi hai)
        save_path = f"downloads/{track.id}.mp3"
        try:
            async with self.client.stream("GET", track.cdnurl) as response:
                if response.status_code != 200:
                    return None
                
                async with aiofiles.open(save_path, "wb") as f:
                    # 1MB chunk size for high-speed write
                    async for chunk in response.aiter_bytes(chunk_size=1048576):
                        await f.write(chunk)
            return save_path
        except Exception as e:
            logger.error(f"Direct Download Fail: {e}")
            return None

    async def close(self):
        """Client band karne ke liye"""
        await self.client.aclose()

# --- Example Usage ---
"""
async def main():
    api = FallenApi("https://your-api.com", "your_key")
    file = await api.download_track("Faded Alan Walker")
    if file:
        print(f"Downloaded: {file}")
    await api.close()

if __name__ == "__main__":
    asyncio.run(main())
"""
