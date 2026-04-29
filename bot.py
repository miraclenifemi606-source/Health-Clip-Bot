import os
import whisper
import yt_dlp
from telegram.ext import Updater, MessageHandler, Filters
from clipper import create_clip
from analyzer import find_hooks
from utils import clean_up

TOKEN = os.getenv("BOT_TOKEN")

model = whisper.load_model("base")


def download_video(url):
    filename = "video.mp4"
    ydl_opts = {
        "outtmpl": filename,
        "format": "mp4"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename


def process(update, context):
    url = update.message.text
    chat_id = update.message.chat_id

    update.message.reply_text("Downloading video...")

    video_path = download_video(url)

    update.message.reply_text("Analyzing health content...")

    result = model.transcribe(video_path)
    transcript = result["text"]

    hooks = find_hooks(transcript)

    clips_sent = 0

    for i, (start, end) in enumerate(hooks):
        output = f"clip_{i}.mp4"

        create_clip(video_path, start, end, output)

        update.message.reply_video(
            video=open(output, "rb"),
            caption=f"🎬 Clip {i+1}\nHealth Insight Clip\n#health #medical #nursing"
        )

        clean_up(output)
        clips_sent += 1

    clean_up(video_path)

    update.message.reply_text(f"Done! {clips_sent} clips generated.")


updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process))

updater.start_polling()
updater.idle()
