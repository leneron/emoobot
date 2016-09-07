# main script for handling the messages
# serves many users with the standart asynchronous module
# more effective than blocking algorithms
import asyncio
import telepot
from telepot.aio.delegate import per_chat_id, create_open
from bayes_classifier import BayesClassifier
from data_editor import Editor


# class that replies messages
class MessageHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(MessageHandler, self).__init__(seed_tuple, timeout)
        MessageHandler.classifier = BayesClassifier('data_examples/', '_')

    # await suspends on_message(...) execution
    # until self.sender.sendMessage(...) completes
    async def on_chat_message(self, msg):
        # handling the incoming message and computing the correct response
        c = MessageHandler.classifier.getClass(Editor.clean(msg['text']))
        await self.sender.sendMessage(c)

# creating the bot

TOKEN = '244035013:AAHXbdprTeisw3hAUWX7VJehWkThR3WwIzk' # bot's own token

# DelegatorBot is a factory
#
# it constructs a new bot,
# if the bot with the same seed(identifier, per_char_id()) doesn't exist
# and seed is hashable
#
# it helps to avoid blocking while listening to the different chats
#
# if no message is captured after TIME seconds,
# delegate is destroyed
#
# more in the documentation:
# https://github.com/nickoala/telepot/blob/master/REFERENCE.md#telepot-DelegatorBot

TIME = 10

bot = telepot.aio.DelegatorBot(TOKEN, [
    (per_chat_id(),
     create_open(MessageHandler, timeout=TIME)),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening...')

loop.run_forever()