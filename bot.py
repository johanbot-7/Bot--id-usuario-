from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7904869791:AAF5BWsCCaXjbydOX49PW94n3n1riTt1MZ8"
ADMIN_ID = 7957443258  # tu ID
GRUPO_LOGS = -1001234567890  # opcional (puedes quitarlo si no quieres logs)

usuarios_bloqueados = set()


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id in usuarios_bloqueados:
        await update.message.reply_text("❌ Estás bloqueado.")
        return

    keyboard = [
        [InlineKeyboardButton("🆔 Ver mi ID", callback_data="ver_id")],
        [
            InlineKeyboardButton("🔒 Función 2", callback_data="func2"),
            InlineKeyboardButton("🔒 Función 3", callback_data="func3"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📋 Menú:\nSelecciona una opción:",
        reply_markup=reply_markup
    )


# BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data

    await query.answer()

    if user.id in usuarios_bloqueados:
        await query.edit_message_text("❌ Estás bloqueado.")
        return

    # BOTÓN PÚBLICO
    if data == "ver_id":
        await query.edit_message_text(f"🆔 Tu ID es: {user.id}")

        try:
            await context.bot.send_message(
                chat_id=GRUPO_LOGS,
                text=f"👤 {user.first_name} ({user.id}) usó VER ID"
            )
        except:
            pass

    # BOTONES PRIVADOS
    elif data in ["func2", "func3"]:
        if user.id != ADMIN_ID:
            await query.answer("❌ No tienes permiso", show_alert=True)
            return

        if data == "func2":
            await query.edit_message_text("✅ Ejecutaste Función 2")
        elif data == "func3":
            await query.edit_message_text("✅ Ejecutaste Función 3")

        try:
            await context.bot.send_message(
                chat_id=GRUPO_LOGS,
                text=f"👑 ADMIN {user.first_name} ({user.id}) usó {data}"
            )
        except:
            pass


# /id (sirve en privado y en grupos)
async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type in ["group", "supergroup"]:
        await update.message.reply_text(f"🆔 ID del grupo:\n{chat.id}")
    else:
        await update.message.reply_text(f"🆔 Tu ID:\n{chat.id}")


# bloquear usuario
async def bloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        uid = int(context.args[0])
        usuarios_bloqueados.add(uid)
        await update.message.reply_text(f"🚫 Usuario {uid} bloqueado")
    except:
        await update.message.reply_text("Uso: /bloquear ID")


# desbloquear usuario
async def desbloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        uid = int(context.args[0])
        usuarios_bloqueados.discard(uid)
        await update.message.reply_text(f"✅ Usuario {uid} desbloqueado")
    except:
        await update.message.reply_text("Uso: /desbloquear ID")


# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("id", id))
app.add_handler(CommandHandler("bloquear", bloquear))
app.add_handler(CommandHandler("desbloquear", desbloquear))
app.add_handler(CallbackQueryHandler(botones))

app.run_polling()
