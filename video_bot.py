import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import asyncio

BOT_TOKEN = "8288599599:AAFSh94H0ODyuNyE9LndZy7lGotimeoCAvk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Helper function to download video ---
def download_video(url):
    try:
        if not os.path.exists("downloads"):
            os.mkdir("downloads")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        return file_name
    except Exception as e:
        print("Download error:", e)
        return None


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Hello! Send me any YouTube or Instagram video link, and I’ll send it back in the best quality available 🎥")


@dp.message()
async def handle_links(message: Message):
    text = message.text.strip()

    if any(x in text for x in ["youtube.com", "youtu.be", "instagram.com", "reel"]):
        await message.answer("📥 Downloading video, please wait...")

        video_path = download_video(text)

        if video_path and os.path.exists(video_path):
            try:
                video_file = FSInputFile(video_path)
                await message.answer_video(video=video_file)
                os.remove(video_path)
            except Exception as e:
                await message.answer(f"⚠️ Could not send video: {e}")
        else:
            await message.answer("❌ Sorry, I couldn't download this video. It may be private or restricted.")


async def main():
    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
