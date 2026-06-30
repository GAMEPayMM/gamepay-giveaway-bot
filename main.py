import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import TOKEN, CHANNEL_USERNAME, ADMIN_ID
from db import *


async def post_init(application: Application):
    await init_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    member = await context.bot.get_chat_member(
        CHANNEL_USERNAME,
        user.id
    )

    if member.status in ["left", "kicked"]:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ You must join our channel first.",
            reply_markup=reply_markup
        )

        return

    joined = await add_entry(user)

    if joined:
        await update.message.reply_text(
            "✅ Giveaway Entry Successful!"
        )
    else:
        await update.message.reply_text(
            "⚠️ You have already joined this giveaway."
        )


async def entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total = await count_entries()

    await update.message.reply_text(
        f"📊 Entries : {total}"
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

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage : /draw 3"
        )
        return

    winners = int(context.args[0])

    users = await all_entries()

    if len(users) == 0:
        await update.message.reply_text(
            "No Entries."
        )
        return

    if winners > len(users):
        winners = len(users)

    selected = random.sample(users, winners)

    text = "🏆 Giveaway Winners\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, u in enumerate(selected):

        if u[1]:
            name = f"@{u[1]}"
        else:
            name = u[2]

        medal = medals[i] if i < 3 else "🎉"

        text += f"{medal} {name}\n"

    text += f"\n👥 Total Entries : {len(users)}"

    await update.message.reply_text(text)


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
