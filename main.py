import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Barka da zuwa Video Converter Bot!\n\n"
        "Turo min da video, zan taimaka maka wajen converting/rendering."
    )

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    await message.reply_text("⏳ Ana karɓar video...")

    file = await message.video.get_file()
    input_file = f"/tmp/{message.video.file_unique_id}.mp4"
    output_file = f"/tmp/converted_{message.video.file_unique_id}.mp4"

    await file.download_to_drive(input_file)

    await message.reply_text("🔄 Ana converting/rendering video...")

    try:
        subprocess.run([
            "ffmpeg",
            "-i", input_file,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            output_file,
            "-y"
        ], check=True)

        await message.reply_text("✅ An gama! Ana tura maka video...")

        with open(output_file, "rb") as video:
            await message.reply_video(video)

        os.remove(input_file)
        os.remove(output_file)

    except Exception as e:
        await message.reply_text(f"❌ An samu matsala: {e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    print("Bot yana aiki...")
    app.run_polling()


if name == "main":
    main()
