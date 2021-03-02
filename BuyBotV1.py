import discord
import unbelievaboat as unb 
import time

BNOS = '755540442371719220'
TS = '793659768606425140'
Josh = '710217407054217326'
Ryan = '701063208496136242'
Veer = '798528159610830898'
Wes = '708727850223534111'
Willie = '741059322489864202'
BuyBot = '802709569478328360'


client = discord.Client() 
bot = unb.client('unbelievaboat API token')

grubcoin = 40
tenio_electric_car = 11
tenio_solar_panel = 10
mbc_flippers = 5
mbc_aqua_breather = 15
mbc_day_guide = 30
mbc_boat = 75
mbc_week_guide = 100
mbc_bundle = 200

@client.event
async def on_message(message):
  global grubcoin
  if message.author == client.user:
    return
  if message.content == '!buy grubcoin' or message.content == '!buy-item grubcoin' or message.content == '!buy Grubcoin' or message.content =='!buy-item grubcoin':
    time.sleep(2)
    bot.change_user_bal(BNOS, Josh, cash=0, bank=grubcoin, reason='grubcoin transaction')
    grubcoin*=1.2
    print(str(int(grubcoin))+'-grubcoin')
    RyanDM = await bot.fetch_channel(800516945522065438)
    await RyanDM.send(str(int(grubcoin))+'-grubcoin price')

  if message.content == '!buy TENIO Electric Car' or message.content == '!buy Electric Car' or message.content == '!buy electric car' or message.content == '!buy tenio electric car' or message.content == '!buy car' or message.content == '!buy-item TENIO Electric Car' or message.content == '!buy-item Electric Car' or message.content == '!buy-item electric car' or message.content == '!buy-item tenio electric car' or message.content == '!buy-item car':
    time.sleep(2)
    TEC_fee = int(0.2*tenio_electric_car)
    TEC_profit = tenio_electric_car-TEC_fee
    bot.change_user_bal(BNOS, Veer, cash=0, bank=TEC_profit, reason='EV Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=TEC_fee, reason='BuyBot fee')

  if message.content == '!buy TENIO Solar Panel' or message.content == '!buy Solar Panel' or message.content == '!buy solar panel' or message.content == '!buy tenio solar panel' or message.content == '!buy panel' or message.content == '!buy-item TENIO Solar Panel' or message.content == '!buy-item Solar Panel' or message.content == '!buy-item solar panel' or message.content == '!buy-item tenio solar panel' or message.content == '!buy-item panel':
    time.sleep(2)
    TSP_fee = int(0.2*tenio_solar_panel)
    TSP_profit = tenio_solar_panel-TSP_fee
    bot.change_user_bal(BNOS, Veer, cash=0, bank=TSP_profit, reason='Solar Panel Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=TSP_fee, reason='BuyBot fee')

  if message.content == '!buy MBC Flippers' or message.content == '!buy mbc flippers' or message.content == '!buy flippers' or message.content == '!buy-item MBC Flippers' or message.content == '!buy-item mbc flippers' or message.content == '!buy-item flippers':
    time.sleep(2)
    MF_fee = int(0.2*mbc_flippers)
    MF_profit = mbc_flippers-MF_fee
    print(MF_fee)
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MF_profit, reason='Flippers Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MF_fee, reason='BuyBot fee')

  if message.content == '!buy MBC Aqua-Breather' or message.content == '!buy mbc aqau-breather' or message.content == '!buy aqua-breather' or message.content == '!buy-item MBC Aqua-Breather' or message.content == '!buy-item mbc aqau-breather' or message.content == '!buy-item aqua-breather':
    time.sleep(2)
    MAB_fee = int(0.2*mbc_aqua_breather)
    MAB_profit = mbc_aqua_breather-MAB_fee
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MAB_profit, reason='Aqua-breather Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MAB_fee, reason='BuyBot fee')

  if message.content == '!buy MBC 1 Day Guide' or message.content == '!buy mbc 1 day guide' or message.content == '!buy 1 Day Guide' or message.content == '!buy 1 day guide' or message.content == '!buy Day Guide' or message.content == '!buy day guide' or message.content == '!buy-item MBC 1 Day Guide' or message.content == '!buy-item mbc 1 day guide' or message.content == '!buy-item 1 Day Guide' or message.content == '!buy-item 1 day guide' or message.content == '!buy-item Day Guide' or message.content == '!buy-item day guide':
    time.sleep(2)
    MDG_fee = int(0.2*mbc_day_guide)
    MDG_profit = mbc_day_guide-MDG_fee
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MDG_profit, reason='Day Guide Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MDG_fee, reason='BuyBot fee')
  
  if message.content == '!buy MBC Boat' or message.content == '!buy mbc boat' or message.content == '!buy Boat' or message.content == '!buy boat' or message.content == '!buy-item MBC Boat' or message.content == '!buy-item mbc boat' or message.content == '!buy-item Boat' or message.content == '!buy-item boat':
    time.sleep(2)
    MB_fee = int(0.2*mbc_boat)
    MB_profit = mbc_boat-MB_fee
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MB_profit, reason='Boat Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MB_fee, reason='BuyBot fee')

  if message.content == '!buy MBC 1 Week Guide' or message.content == '!buy mbc 1 week guide' or message.content == '!buy 1 Week Guide' or message.content == '!buy 1 week guide' or message.content == '!buy Week Guide' or message.content == '!buy week guide' or message.content == '!buy-item MBC 1 Week Guide' or message.content == '!buy-item mbc 1 week guide' or message.content == '!buy-item 1 Week Guide' or message.content == '!buy-item 1 week guide' or message.content == '!buy-item Week Guide' or message.content == '!buy-item week guide':
    time.sleep(2)
    MWG_fee = int(0.2*mbc_week_guide)
    MWG_profit = mbc_week_guide-MWG_fee
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MWG_profit, reason='Week Guide Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MWG_fee, reason='BuyBot fee')

  if message.content == '!buy MBC Scuba Bundle' or message.content == '!buy mbc scuba bundel' or message.content == '!buy Scuba Bundle' or message.content == '!buy scuba bundle' or message.content == '!buy Bundle' or message.content == '!buy bundle' or message.content == '!buy-item MBC Scuba Bundle' or message.content == '!buy-item mbc scuba bundel' or message.content == '!buy-item Scuba Bundle' or message.content == '!buy-item scuba bundle' or message.content == '!buy-item Bundle' or message.content == '!buy-item bundle':
    time.sleep(2)
    MSB_fee = int(0.2*mbc_bundle)
    MSB_profit = mbc_bundle-MSB_fee
    bot.change_user_bal(BNOS, Wes, cash=0, bank=MSB_profit, reason='Scuba Bundle Sale')
    bot.change_user_bal(BNOS, BuyBot, cash=0, bank=MSB_fee, reason='BuyBot fee')

client.run('discord API token')
