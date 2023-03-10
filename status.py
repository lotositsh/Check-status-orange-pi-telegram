import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a Telegram bot instance
bot = Bot(token='YOUR_TOKEN_HERE')

# Set up the dispatcher
dp = Dispatcher(bot)

# Define the handler for the /status command
@dp.message_handler(Command('status'))
async def status(message: types.Message):
    user_id = message.from_user.id
    allowed_user_id = 777777777  # Replace with your user ID

    if user_id != allowed_user_id:
        await message.answer("You are not authorized to run this command.")
        return
    # Run the command to get system status and store the output
    cmd_output = os.popen(
        "free -m | awk 'NR==2{printf \"RAM: %s/%sMB (%.2f%%)\\n\", $3,$2,$3*100/$2 }' && "
        "df -h | awk '$NF==\"/\"{printf \"SD: %d/%dGB (%s)\\n\", $3,$2,$5}' && "
        "echo 'Temp: ' && cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"%.1f°C\\n\", $1/1000}' && "
        # "echo 'CPU usage: ' && mpstat -P ALL | awk '{if($2 ~ /[0-9]+/ && $2 < 4) print \"CPU\",$2\":\",100-$NF\"%\"}' && "
        "echo 'IP address: ' && curl -s ifconfig.co && echo ' ('$(curl -s ifconfig.co/country)')'",
        "r").read()

    # Send the output back to the user
    await message.answer(cmd_output)

# Start the bot
if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
