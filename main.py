import random

from config import TOKEN, CHANNEL_USERNAME, ADMIN_ID
from db import *

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    member = await context.bot.get_chat_member(
        CHANNEL_USERNAME,
        user.id
    )

    if member.status in ["left", "kicked"]:
        await update.message.reply_text(
            f"❌ Please join {CHANNEL_USERNAME} first."
        )
        return

    await add_entry(user)

    await update.message.reply_text(
        "✅ Giveaway Entry Successful!"
    )


async def entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total = await count_entries()

    await update.message.reply_text(
        f"Entries: {total}"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await reset_entries()

    await update.message.reply_text(
        "✅ Reset Complete."
    )


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /draw <number>"
        )
        return

    winners = int(context.args[0])

    users = await all_entries()

    if len(users) == 0:
        await update.message.reply_text(
            "No entries found."
        )
        return

    if winners > len(users):
        winners = len(users)

    selected = random.sample(users, winners)

    text = "🏆 Winners\n\n"

    for i, u in enumerate(selected):
        username = u[1] if u[1] else u[2]
        text += f"{i+1}. {username}\n"

    await update.message.reply_text(text)


async def post_init(application: Application):
    await init_db()


app = (
    Application.builder()
    .token(TOKEN)
    .post_init(post_init)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("entries", entries))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("draw", draw))

app.run_polling()
