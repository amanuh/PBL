import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


app = Client("chat_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)


keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Project Details", callback_data="details")]])
keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])


#startcmd
@app.on_message(filters.command("start"))
async def start(Client,message):
    await message.reply_text(config.Message,reply_markup=keyboard)


#ai response
@app.on_message(filters.private | filters.group)
async def handle_message(client: Client, message: Message):    
    if message.from_user and message.from_user.is_bot:
        return
    
    if message.chat.type in ["group", "supergroup"]:
        bot_username = (await client.get_me()).username
        if not message.text.startswith(f"@{bot_username}"):
            return
        message_text = message.text.replace(f"@{bot_username}", "").strip()
    else:
        message_text = message.text.strip()

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    loading_message = await message.reply_text("⏳ Generating response...")
    try:
        
        response = model.generate_content([f"not GeminiAI but Chat bot,summarized responses ", message_text])
        answer = response.text.strip()
    except Exception as e:
        answer = f"⚠️ Error generating response: {str(e)}"

    
    await loading_message.edit_text(answer)


#callbacks
@app.on_callback_query()
async def callback_query(Client, callback_query):
    if callback_query.data == "details":
        await callback_query.message.edit_text(config.details,reply_markup=keyboard2)
    elif callback_query.data == "back":
        await callback_query.message.edit_text(config.Message,reply_markup=keyboard)
    else:
        await callback_query.answer("Callback Error", show_alert=True)


#start bot
print("Bot is running ")
app.run()
