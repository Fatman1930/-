from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# Replace with your own bot token
BOT_TOKEN = '7935547453:AAF_zjzOo0R-rzuQFo6-mj2hO9EuZVpy_1E'

# Function to download video
def download_video(url):
    output_path = "C:/Users/ahmed/Videos/telegram_downloads"
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best[ext=mp4]',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid video URL.")
        return

    await update.message.reply_text("Downloading the video...")

    try:
        file_path = download_video(url)
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)  # Optional: delete after sending
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Start bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
