import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from downloader import download_video
from transcriber import process_video_to_text
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- /start command handler ---
def start(update: Update, context: CallbackContext):
    welcome_text = (
        "👋 Hello! I am a **Video Transcriber Bot**.\n\n"
        "📌 Send me a direct video link (like a YouTube video), and I'll download the video, "
        "extract the audio, and give you the transcript!\n\n"
        "✅ Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    update.message.reply_text(welcome_text, parse_mode='Markdown')

# --- Message handler for links ---
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id

    # Check if message looks like a URL
    if not (url.startswith("http://") or url.startswith("https://")):
        update.message.reply_text("❌ That doesn't look like a valid link. Please send a direct video URL.")
        return

    try:
        update.message.reply_text("📥 Downloading video, please wait...")
        video_path = download_video(url)

        update.message.reply_text("🎧 Extracting audio and transcribing... This may take a minute.")
        transcript = process_video_to_text(video_path)

        # Telegram messages have a character limit (4096). Send in chunks if needed.
        for i in range(0, len(transcript), 4096):
            update.message.reply_text(transcript[i:i+4096])

        update.message.reply_text("✅ Done! If you want to transcribe another video, just send the link.")

    except Exception as e:
        update.message.reply_text(f"⚠️ Oops! Something went wrong:\n`{str(e)}`", parse_mode='Markdown')

# --- Main ---
def main():
    print("🚀 Bot is running...")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
