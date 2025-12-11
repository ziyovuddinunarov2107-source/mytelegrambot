import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8587053118:AAEt3SN-HgNSVjVvemt95UNF9-mCiOCu2KI"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any YouTube or Instagram video link.")


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("Downloading, please wait...")

    # Output file name
    output_file = "downloaded_video.mp4"

    # yt-dlp settings
    ydl_opts = {
        "outtmpl": output_file,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
    }

    try:
        # Remove previous file if exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send to user
        await update.message.reply_video(video=open(output_file, "rb"))

        # Delete file after sending
        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

