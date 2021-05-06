# import telebot
# from .settingTelegramBot import *
# import json
#
# class TelegramBot(object):
#     bot = telebot.TeleBot(TOKEN_BOT, parse_mode='HTML')
#
#     # def SendMessage(self, message):
#         # self.bot.send_message(ID_CHAT, message)
#
#     def UpdateBot(self, request):
#         jsonMessage = json.loads(request.body)
#         update = telebot.types.Update.de_json(jsonMessage)
#         self.bot.process_new_updates(update)