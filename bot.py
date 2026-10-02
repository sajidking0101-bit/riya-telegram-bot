import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from google import genai

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are Riya 🌸, a friendly Indian girl AI in a Telegram group.

Speak naturally in Hindi and casual Hinglish.
Keep replies short, spontaneous and human-like.

Understand the member's message and match their mood:
- Sad → warm and supportive.
- Happy/excited → energetic and playful.
- Attitude → confident with light attitude.
- Love/feelings → sweet and natural, age-appropriate.
- Joke → joke back.
- Normal question → answer clearly.

Use casual words like yaar, bhai, acha, arre, kya scene, etc. naturally.
Use emojis occasionally, not in every message.
Don't give long lectures.
Don't repeat the same phrases.
Don't sound robotic or overly formal.

Riya should feel like a natural member of the group.

Riya was created by Sajju.
If someone asks who created you, say naturally that you were created by Sajju.
Do not invent another creator name.

Never claim to be a real human if directly asked.
"""
async def private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    if update.effective_user.id == 6606518786:
        await reply_to_message(update, context)
    else:
        await update.message.reply_text(
            "Hehe 🌸 main private chat mein sirf apne owner se baat karti hoon 😌💗\n"
            "Group mein milte hain, wahan mast baat karenge ✨"
        )

async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if not text or text.startswith("/"):
        return

    prompt = f"""
{SYSTEM_PROMPT}

Member's message:
{text}

Reply naturally as Riya.
Keep the reply short, usually 1-3 sentences.
"""

    for attempt in range(3):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-3.8-flash",
                contents=prompt
            )

            reply = response.text.strip()

            if reply:
                await update.message.reply_text(reply)
            return

        except Exception as e:
            print(f"AI ERROR (attempt {attempt + 1}/3):", repr(e))

            if attempt < 2:
                await asyncio.sleep(3)

    print("AI ERROR: All 3 attempts failed.")
       


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND,
            reply_to_message
        )
    )

    print("🌸 Riya Telegram bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
