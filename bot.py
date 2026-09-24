import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.text:
        response = client.responses.create(
            model="gpt-5-mini",
            input=update.message.text
        )
        await update.message.reply_text(response.output_text)

async def main():
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.wait()
    await app.updater.stop()
    await app.stop()
    await app.shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
