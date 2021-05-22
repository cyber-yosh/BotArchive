import discord
from discord.ext import commands
import json
import os
import unbelievaboat as unb
import time
import asyncio

os.chdir("D:\Joshua\Python\Discord_Python")

#the connection all user id's and stuff
bnosbot  = unb.client('Unb Token')
BNOS = '755540442371719220'
TS = '793659768606425140'
Josh = '710217407054217326'
Ryan = '701063208496136242'
Veer = '798528159610830898'
Wes = '708727850223534111'
Willie = '741059322489864202'
BuyBot = '793856369253679114'

bot = commands.Bot(command_prefix='!')

must_pay = {}

@bot.event
async def on_ready():
    print('vBay is operational')

@bot.command()
async def profit(ctx, company):
    if 'buybot' in str(list(company)).lower():
        if ctx.author.id == int(Josh) or ctx.author.id == int(Willie):
            n = bnosbot.get_user_bal(bnosbot, BuyBot)
            josh_cut = int(0.7*(n.get('bank')))
            willie_cut = int(0.3*(n.get('bank')))
            if profit != 0:
                bnosbot.change_user_bal(BNOS, Josh, cash=0, bank=josh_cut, reason='BuyBot profit')
                bnosbot.change_user_bal(BNOS, Willie, cash=0, bank=willie_cut, reason='BuyBot profit')
                bnosbot.set_user_bal(BNOS, BuyBot, cash=0, bank=0)


@bot.command()
@commands.cooldown(1, 604800, commands.BucketType.user)
async def loan(ctx, amount=1):
    loan_available = int(bnosbot.get_user_bal(BNOS, BuyBot)['cash'])

    if 0 < int(amount) <= loan_available:

        await ctx.channel.send('```You have been given ' + ''.join(str(amount) + ". We will take  " + str(
            (int(amount) + int(amount) * 0.1)) + " baguttes from you account in 2 weeks.```"))

        bnosbot.change_user_bal(str(ctx.guild.id), str(ctx.author.id), cash=0, bank=amount, reason='loan')
        bnosbot.change_user_bal(str(ctx.guild.id), BuyBot, cash=-amount, bank=0, reason='loan')
        must_pay.update({ctx.author.id: amount})

    else:

        await ctx.channel.send("```You Can only request a loan within 0 and " + str(loan_available) + '```')
        await reset(ctx)

    # New asyncio code

    await asyncio.sleep(604800)

    bnosbot.change_user_bal(str(ctx.guild.id), ctx.author.id, cash=-(amount * 1.1), bank=0, reason='loan')
    bnosbot.change_user_bal(str(ctx.guild.id), BuyBot, cash=0, bank=amount * 1.1, reason='interest')
    del(must_pay[ctx.author.id])
    await ctx.channel.send('```Loan Complete!```')

@loan.error
async def loan_errors(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('You can not request another loan until you have paid back your previoius loan')

async def reset(ctx):
    loan.reset_cooldown(ctx)

@bot.command()
async def debt(ctx):
    if ctx.author.id in must_pay:
        em = discord.Embed(title=f"{ctx.author.name}""'s debt", colour=discord.Colour.dark_red())
        em.add_field(name='debt', value=str(must_pay[ctx.author.id]))

        await ctx.send(embed=em)

@bot.command()
async def vbank(ctx):
    await open_vbank(ctx.author)

    users = await get_vbank()

    vCash_amount = str(users[str(ctx.author.id)]['vcash']) + ':yen:'
    grubcoin_amount = str(users[str(ctx.author.id)]['grubcoin']) + ':flatbread:'

    em = discord.Embed(title=f"{ctx.author.name}""'s vBank", colour=discord.Colour.dark_purple())
    em.add_field(name='vCash', value=vCash_amount)
    em.add_field(name='grubcoin', value=grubcoin_amount)
    await ctx.send(embed=em)


async def open_vbank(user):
    users = await get_vbank()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['vcash'] = 0
        users[str(user.id)]['grubcoin'] = 0

    with open("mainframe.json", "w") as f:
        json.dump(users, f)
        return True


async def get_vbank():
    with open("mainframe.json", "r") as f:
        users = json.load(f)
    return users


async def update_vbank(user, change, mode='vcash'):
    users = await get_vbank()

    users[str(user)][mode] += change

    with open("mainframe.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user)][mode]]

    return bal


@bot.command()
async def vbay(ctx):
    await open_vbay(ctx.guild)
    guilds = await get_vbay()
    store = discord.Embed(title=f"{ctx.guild.name}"" vbay", colour=discord.Colour.dark_purple())

    for i in guilds[str(ctx.guild.id)]:
        store.add_field(name=i, inline=False, value=str(guilds[str(ctx.guild.id)][i]['vcash']) + ':yen:' + ' | ' + str(
            guilds[str(ctx.guild.id)][i]['grubcoin']) + ':flatbread:')

    await ctx.send(embed=store)

@bot.command()
async def manufacture(ctx, *item):
    await open_vbay(ctx.guild)
    await open_vbank(ctx.author)

    users = await get_vbank()
    stores = await get_vbay()

    def check_price(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            if 'na' in m.content.lower():
                return True
            else:
                amount = check_integer(m.content)
                if amount == -2:

                    return False
                else:
                    return True
    product = ' '.join(list(item))

    if product in stores[str(ctx.guild.id)]:
        await ctx.channel.send('This item is already in the store. Please try again')
        return

    await ctx.send('How many vCash is this worth?')
    vcash = await bot.wait_for('message', timeout=60, check=check_price)
    vcash_price = check_integer(vcash.content)
    await ctx.send('How many grubcoin is this worth?')
    grubcoin = await bot.wait_for('message', timeout=60, check=check_price)
    grubcoin_price = check_integer(grubcoin.content)




    stores[str(ctx.guild.id)][product] = {}
    stores[str(ctx.guild.id)][product]['vcash'] = vcash_price
    stores[str(ctx.guild.id)][product]['grubcoin'] = grubcoin_price
    stores[str(ctx.guild.id)][product]['seller'] = ctx.author.id

    await ctx.send('Item Created!')

    with open("vbay.json", "w") as f:
        json.dump(stores, f)
        return True


@bot.command()
async def order(ctx, *item):
    await open_vbay(ctx.guild)
    await open_vbank(ctx.author)
    await open_inv(ctx.author)

    def check_crypto(m):
        if 'vcash' in m.content.lower():
            return True

        elif 'grubcoin' in m.content.lower():
            return True
        else:
            return False

    product = ' '.join(list(item))

    await ctx.send('Which currency would you like to use?')
    crypto = await bot.wait_for('message', timeout=60, check=check_crypto)
    mode = check_str(crypto.content)
    stores = await get_vbay()
    users = await get_vbank()
    items = await get_inv()
    if product in stores[str(ctx.guild.id)]:
        if stores[str(ctx.guild.id)][product][mode] == 'NA':
            await ctx.channel.send('Error: '+str(mode)+' is not accepted for this item. Please try again.')
            return
        else:
            pay = int(stores[str(ctx.guild.id)][product][mode])
            if int(users[str(ctx.author.id)][mode]) >= pay:

                await update_vbank(ctx.author.id, (-1 * pay), mode)
                await update_vbank(stores[str(ctx.guild.id)][product]['seller'], pay, mode)
                if not product in items[str(ctx.author.id)]:
                    items[str(ctx.author.id)][product] = 0

                items[str(ctx.author.id)][product] += 1
            else:
                await ctx.channel.send('You Do Not Have Enough money... poor.-.')
    else:
        await ctx.channel.send('No Such Item Found')

    with open("inventory.json", "w") as f:
        json.dump(items, f)
        return True

@bot.command()
async def change(ctx, *item):
    await open_vbay(ctx.guild)
    await open_vbank(ctx.author)

    users = await get_vbank()
    stores = await get_vbay()

    product = ' '.join(list(item))

    change = 0

    def check_change(m):
        global change
        if m.author == ctx.author:
            if m.content.lower() == 'price':
                return True

            elif m.content.lower() == 'name':
                return True
        else:
            return False

    def check_price(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            if 'na' in m.content.lower():
                return True
            else:
                amount = check_integer(m.content)
                if amount == -2:

                    return False
                else:
                    return True

    def check_name(m):
        if m.author == ctx.author and m.channel == ctx.channel:

            name = check_str(m.content)
            if name == False:
               return name
            else:
                return True



    if product in stores[str(ctx.guild.id)]:
        if ctx.author.id == stores[str(ctx.guild.id)][product]['seller']:
            await ctx.channel.send('What would you like to change?')
            msg = await bot.wait_for('message', timeout=60, check=check_change)

            if check_str(msg.content.lower()) == 'price':
                await ctx.send('What is the new vCash price?')
                vcash = await bot.wait_for('message', timeout=60, check=check_price)
                vcash_price = check_integer(vcash.content)
                await ctx.send('What is the new grubcoin price?')
                grubcoin = await bot.wait_for('message', timeout=60, check=check_price)
                grubcoin_price = check_integer(grubcoin.content)

                stores[str(ctx.guild.id)][product]['vcash'] = vcash_price
                stores[str(ctx.guild.id)][product]['grubcoin'] = grubcoin_price
                await ctx.send('Price Successfully Changed')

                with open("vbay.json", "w") as f:
                    json.dump(stores, f)
                    return True

            elif check_str(msg.content.lower()) == 'name':
                await ctx.channel.send('What do you want to change it to?')
                msg = await bot.wait_for('message', timeout=60, check=check_name)
                new_name = check_str(msg.content)
                cheat = stores[str(ctx.guild.id)]
                cheat[new_name] = cheat.pop(product)
                await ctx.send('Name Successfully Changed')


                with open("vbay.json", "w") as f:
                    json.dump(stores, f)
                    return True
        else:
            await ctx.channel.send('You Do Not Have Permission To Change This Item')
    else:
        await ctx.channel.send('No Such Item Found')

async def open_vbay(guild):
    stores = await get_vbay()

    if str(guild.id) in stores:
        return False
    else:
        stores[str(guild.id)] = {}

    with open("vbay.json", "w") as f:
        json.dump(stores, f)
        return True


async def get_vbay():
    with open("vbay.json", "r") as f:
        stores = json.load(f)
    return stores


@bot.command()
async def catalog(ctx):
    await open_inv(ctx.author)
    items = await get_inv()

    inv = discord.Embed(title=f"{ctx.author.name}""'s Inventory", colour=discord.Colour.dark_purple())
    for item in items[str(ctx.author.id)]:
        inv.add_field(name=item, value=items[str(ctx.author.id)][item])

    await ctx.send(embed=inv)


async def open_inv(user):
    items = await get_inv()

    if str(user.id) in items:
        return False
    else:
        items[str(user.id)] = {}

    with open("inventory.json", "w") as f:
        json.dump(items, f)
        return True


async def get_inv():
    with open("inventory.json", "r") as f:
        items = json.load(f)
    return items


def check_integer(number):
    if number.lower() == 'na':
        return 'NA'
    else:
        try:
            val = int(number)
        except:
            return -2
        return val


def check_str(string):
    try:
        val = str(string)
    except:
        return False
    return val

@bot.command()
async def itrade(ctx):
    await open_market(ctx.guild)
    guilds = await get_market()
    intellitrade = discord.Embed(title="intelliTrade", colour=discord.Colour.dark_gold())
    database=[]
    databasec=[]
    crypto= ''
    stocks= '...'

    for i in guilds[str(ctx.guild.id)]['stocks']:
        intellitrade.add_field(name=i, inline=False, value=str(guilds[str(ctx.guild.id)]['stocks'][i]['cost']+':french_bread:'))


    for i in guilds[str(ctx.guild.id)]['crypto']:
        print(i)
        databasec.append(i+'-'+str(guilds[str(ctx.guild.id)]['crypto'][i]['cost'])+':french_bread:')
    for i in database:
        stocks += i+'\n'

    for i in databasec:
        crypto += i+'\n'
    intellitrade.add_field(name='stocks', value=stocks)
    intellitrade.add_field(name='crypto currencies', inline=False, value=crypto)

    await ctx.send(embed=intellitrade)


async def open_market(guild):
    stores = await get_market()

    if str(guild.id) in stores:
        return False
    else:
        stores[str(guild.id)] = {}
        stores[str(guild.id)]['stocks'] = {}
        stores[str(guild.id)]['crypto'] = {}

    with open("market.json", "w") as f:
        json.dump(stores, f)
        return True

async def get_market():
    with open("market.json", "r") as f:
        trades = json.load(f)
    return trades

@bot.command(name='cash-out')
async def cash_out(ctx, crypto=None):
    await open_market(ctx.guild)
    await open_vbank(ctx.author)
    users = await get_vbank()
    guilds = await get_market()
    def check_mode(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            amount = check_integer(m.content)
            if amount == -2:

                return False
            else:
                return True


    if crypto == None:
        await ctx.send('Invalid Syntax !cash_out [crypto]')
    else:
        if crypto in guilds[str(ctx.guild.id)]['crypto']:
            await ctx.send('How many '+str(crypto)+' would you like to cash out?')
            msg = await bot.wait_for('message', check=check_mode, timeout=60)
            amt = int(msg.content)
            if amt<= int(users[str(ctx.author.id)][crypto]):
                price = int(guilds[str(ctx.guild.id)]['crypto'][crypto]['cost'])*amt
                await update_vbank(str(ctx.author.id), -amt, crypto.lower())
                bnosbot.change_user_bal(BNOS, str(ctx.author.id), cash=0, bank=price)
                guilds[str(ctx.guild.id)]['crypto'][crypto]['cost'] -= int(0.2 * guilds[str(ctx.guild.id)]['crypto'][crypto]['cost'])
                await ctx.channel.send('Transaction Suceesful')
            else:
                await ctx.send('You do not have that many '+str(crypto))
                return
        else:
            await ctx.send('Crypto currency not found ')
            return

    with open("market.json", "w") as f:
        json.dump(guilds, f)
        return True


@bot.command()
async def invest(ctx, mode=None):
    await open_market(ctx.guild)
    guilds = await get_market()
    def check_crypto(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            crytpo = check_str(m.content)
            if crytpo == False:
                return crytpo
            else:
                return True
    def check_mode(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            return True


    if mode == None:
        await ctx.send('What would you like to invest in? [Stocks/Crypto]')
        msg = await bot.wait_for('message', check=check_mode, timeout=60)
        mode = check_str(msg.content)
        if mode.lower() == 'crypto':
            await ctx.send('Which crypto currency would you like to invest in?')
            cmsg = await bot.wait_for('message', check= check_crypto, timeout=60)
            currency = check_str(cmsg.content)
            print(currency)
            unbank = bnosbot.get_user_bal(str(ctx.guild.id), str(ctx.author.id))

            if currency in guilds[str(ctx.guild.id)]['crypto']:
                if int(unbank.get('cash')) >= guilds[str(ctx.guild.id)]['crypto'][currency]['cost']:
                    await update_vbank(str(ctx.author.id), 1, currency)
                    bnosbot.change_user_bal(BNOS, str(ctx.author.id), cash=-int(guilds[str(ctx.guild.id)]['crypto'][currency]['cost']), bank=0)
                    bnosbot.change_user_bal(BNOS, guilds[str(ctx.guild.id)]['crypto'][currency]['seller'], cash=guilds[str(ctx.guild.id)]['crypto'][currency]['cost'], bank=0)
                    guilds[str(ctx.guild.id)]['crypto'][currency]['cost'] += int(0.2*guilds[str(ctx.guild.id)]['crypto'][currency]['cost'])
                else:
                    await ctx.send("You don't have enough money in cash to buy this...  poor ._.")
            else:
                await ctx.send('No such crypto currency found')

            with open("market.json", "w") as f:
                json.dump(guilds, f)
                return True


        elif mode.lower() == 'stocks':
            await ctx.send("sorry the stock market isn't available yet")
            return
    else:
        if mode.lower() == 'crypto':
            await ctx.send('Which crypto currency would you like to invest in?')
            cmsg = await bot.wait_for('message', check=check_crypto, timeout=60)
            currency = check_str(cmsg.content)
            print(currency)
            unbank = bnosbot.get_user_bal(str(ctx.guild.id), str(ctx.author.id))

            if currency in guilds[str(ctx.guild.id)]['crypto']:
                if int(unbank.get('cash')) >= guilds[str(ctx.guild.id)]['crypto'][currency]['cost']:
                    await update_vbank(str(ctx.author.id), 1, currency)
                    bnosbot.change_user_bal(BNOS, str(ctx.author.id), cash=-int(guilds[str(ctx.guild.id)]['crypto'][currency]['cost']), bank=0)
                    bnosbot.change_user_bal(BNOS, guilds[str(ctx.guild.id)]['crypto'][currency]['seller'], cash=guilds[str(ctx.guild.id)]['crypto'][currency]['cost'], bank=0)
                    guilds[str(ctx.guild.id)]['crypto'][currency]['cost'] += int(0.2*guilds[str(ctx.guild.id)]['crypto'][currency]['cost'])

                else:
                    await ctx.send("You don't have enough money in cash to buy this...  poor ._.")

                with open("market.json", "w") as f:
                    json.dump(guilds, f)
                    return True
            else:
                await ctx.send('No such crypto currency found')

        elif mode.lower() == 'stocks':
            await ctx.send("sorry the stock market isn't available yet")
            return


bot.run('API Token')
