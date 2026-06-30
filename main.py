import os
import random
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
ContextTypes,
)

from db import *

load_dotenv()

TOKEN=os.getenv("BOT_TOKEN")
CHANNEL=os.getenv("CHANNEL_USERNAME")
ADMIN=int(os.getenv("ADMIN_ID"))

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.effective_user

    member=await context.bot.get_chat_member(
        CHANNEL,
        user.id
    )

    if member.status in ["left","kicked"]:

        await update.message.reply_text(
f"❌ Join {CHANNEL} first."
        )
        return

    await add_entry(
        user.id,
        user.username
    )

    await update.message.reply_text(
"✅ Giveaway Entry Successful!"
    )

async def entries(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id!=ADMIN:
        return

    total=await count_entries()

    await update.message.reply_text(
f"Entries : {total}"
    )

async def reset(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id!=ADMIN:
        return

    await reset_entries()

    await update.message.reply_text(
"Reset Complete."
    )

async def draw(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id!=ADMIN:
        return

    winners=int(context.args[0])

    users=await all_entries()

    if winners>len(users):
        winners=len(users)

    selected=random.sample(users,winners)

    text="🏆 Winners\n\n"

    for i,u in enumerate(selected):

        text+=f"{i+1}. @{u[1]}\n"

    await update.message.reply_text(text)

app=Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("entries",entries))
app.add_handler(CommandHandler("reset",reset))
app.add_handler(CommandHandler("draw",draw))

app.run_polling()
