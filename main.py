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
            f"❌ Join {CHANNEL_USERNAME} first."
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
        f"Entries : {total}"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await reset_entries()

    await update.message.reply_text(
        "Reset Complete."
    )


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    winners = int(context.args[0])

    users = await all_entries()

    if winners > len(users):
        winners = len(users)

    selected = random.sample(users, winners)

    text = "🏆 Winners\n\n"

    for i, u in enumerate(selected):
        text += f"{i+1}. @{u[1]}\n"

    await update.message.reply_text(text)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("entries", entries))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("draw", draw))

app.run_polling()
