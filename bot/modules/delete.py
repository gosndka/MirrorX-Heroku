from telegram.ext import CommandHandler
import threading
from telegram import Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils import gdriveTools

def deletefile(update, context):
	msg_args = update.message.text.split(None, 1)
	msg = ''
	try:
		link = msg_args[1]
		LOGGER.info(msg_args[1])
	except IndexError:
		msg = '⫸ Send a link along with command'

	if msg == '' : 
		drive = gdriveTools.GoogleDriveHelper()
		msg = drive.deletefile(link)
	LOGGER.info(f"this is msg : {msg}")
	reply_message = sendMessage(msg, context.bot, update)

	threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()

delete_handler = CommandHandler(command=BotCommands.deleteCommand, callback=deletefile,
									filters=CustomFilters.owner_filter, run_async=True)
dispatcher.add_handler(delete_handler)
