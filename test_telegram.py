import telepot
token_avp='5757197805:AAGGx88LXt1SZwH4Lycj8KLslzatsNisZc4'
bot = telepot.Bot(token=token_avp)
bot_info =bot.getMe()
print(bot_info)
#chat_id_avp   = 5449371759
chat_id_group  = -1002125490739 # ID DEL GRUPO DE SOPHY
chat_id_group2 = -1002122363347 # ID DEL GRUPO Test_bots
#bot.sendMessage(chat_id_avp,'Little test')
bot.sendMessage(chat_id_group,'Little test')

print("[END]")