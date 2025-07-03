from pathlib import Path
from gigachat import GigaChat
import ssl
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from promts import schemes

### Setup gigachat
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

giga = GigaChat(
    base_url="https://gigachat.devices.sberbank.ru/api/v1",
    credentials=Path("authorization_key.txt").read_text(encoding="utf-8"),
    scope="GIGACHAT_API_PERS",
    ssl_context=ssl_context
)
###
token = Path("token.txt").read_text(encoding="utf-8")

intro = "Ты — лингвист-морфолог.\n"

async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я бот-помощник по русскому языку.\n"
        "Введи /help, чтобы увидеть список комманд")

async def help(update: Update, context):
    await update.message.reply_text(
        "fonet - фонетический разбор\n"
        "morph - морфологический разбор\n"
        "syntax - синтаксический разбор\n"
    )


async def morph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = ' '.join(context.args)
    word = input

    if not word or ' ' in word:
        await update.message.reply_text("Пожалуйста, укажите слово после команды: /morph слово")
    else:
        try:
            response = giga.chat(f"{intro}\nСделай морфологичексий разбор слова: \"{word}\"\nИспользуя одну из схем:\n{schemes["morph"]}\n").choices[0].message.content
        except Exception as e:
            response = f"Ошибка: {str(e)}"

        await update.message.reply_text(response)

async def fonet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = ' '.join(context.args)
    word = input

    if not word or ' ' in word:
        await update.message.reply_text("Пожалуйста, укажите слово после команды: /fonet слово")
    else:
        try:
            response = giga.chat(f"{intro}\nСделай фонетический разбор слова по схеме:\n{schemes["fonet"]}\"{word}\"\n").choices[0].message.content
        except Exception as e:
            response = f"Ошибка: {str(e)}"

        await update.message.reply_text(response)

async def syntax(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = ' '.join(context.args)
    sentence = input

    if not sentence:
        await update.message.reply_text("Пожалуйста, укажите слово после команды: /morph слово")
    else:
        try:
            response = giga.chat(f"{intro}\n{schemes["syntax"]}\"{sentence}\"\n").choices[0].message.content
        except Exception as e:
            response = f"Ошибка: {str(e)}"

        await update.message.reply_text(response)

# Настройка бота
app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("morph", morph))
app.add_handler(CommandHandler("fonet", fonet))
app.add_handler(CommandHandler("syntax", syntax))

# Запуск
print("Polling")
app.run_polling()
