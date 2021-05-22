import discord
from discord.ext import commands
import json
import os
import unbelievaboat as unb
import time


bnosbot  = unb.client('Unbelievaboat API Token')
BNOS = '755540442371719220'
TS = '793659768606425140'
Josh = '710217407054217326'
Ryan = '701063208496136242'
Veer = '798528159610830898'
Wes = '708727850223534111'
Willie = '741059322489864202'
BuyBot = '802709569478328360'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def vbank(ctx):
    await open_vbank(ctx.author)

    users = await get_vbank()

    vCash_amount = str(users[str(ctx.author.id)]['vCash']) + ':yen:'

    em = discord.Embed(title=f"{ctx.author.name}""'s vBank", colour=discord.Colour.dark_purple())
    em.add_field(name='vCash', value=vCash_amount)
    await ctx.send(embed=em)


async def open_vbank(user):
    users = await get_vbank()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['vCash'] = 0

    with open("mainframe.json", "w") as f:
        json.dump(users, f)
        return True


async def get_vbank():
    with open("mainframe.json", "r") as f:
        users = json.load(f)
    return users


async def update_vbank(user, change, mode='vCash'):
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
        store.add_field(name=i, value=str(guilds[str(ctx.guild.id)][i]['vcash']) + ':yen:')

    await ctx.send(embed=store)

@bot.command()
async def manufacture(ctx, item, price=0):
    await open_vbay(ctx.guild)
    await open_vbank(ctx.author)

    users = await get_vbank()
    stores = await get_vbay()

    

    if item in stores[str(ctx.guild.id)]:
        await ctx.channel.send('This item is already in the store. Please try again')
        return


    stores[str(ctx.guild.id)][item] = {}
    stores[str(ctx.guild.id)][item]['vcash'] = price
    stores[str(ctx.guild.id)][item]['seller'] = ctx.author.id


    with open("vbay.json", "w") as f:
        json.dump(stores, f)
        return True


@bot.command()
async def purchase(ctx, item, amount=1):
    await open_vbay(ctx.guild)
    await open_vbank(ctx.author)
    await open_inv(ctx.author)




    stores = await get_vbay()
    users = await get_vbank()
    items = await get_inv()
    if item in stores[str(ctx.guild.id)]:
        
          pay = int(stores[str(ctx.guild.id)][item]['vCash'])
          if int(users[str(ctx.author.id)]['vCash']) >= pay:

              await update_vbank(ctx.author.id, (-1 * pay))
              await update_vbank(stores[str(ctx.guild.id)][item]['seller'], pay)
              if not item in items[str(ctx.author.id)]:
                  items[str(ctx.author.id)][item] = 0

              items[str(ctx.author.id)][item] += 1
          else:
              await ctx.channel.send('You Do Not Have Enough money... poor.-.')
    else:
        await ctx.channel.send('No Such Item Found')

    with open("inventory.json", "w") as f:
        json.dump(items, f)
        return True


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
async def items(ctx):
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


@bot.command()
async def cash_out(ctx, crypto):
    global vcash
    if 'vcash' in str(crypto).lower():
        await open_vbank(ctx.author)

        users = await get_vbank()

        amt = int(users[str(ctx.author.id)]['vCash'])
        if amt != 0:
            crypto_fee = vcash * int(0.2 * amt)
            crypto_profit = vcash * (amt - crypto_fee)
            bnosbot.change_user_bal(BNOS, str(ctx.author.id), cash=0, bank=crypto_profit)
            bnosbot.change_user_bal(BNOS, bnosbot, cash=0, bank=crypto_fee)
            vcash *= 0.8
        else:
            await ctx.channel.send("You don't have any vCash.")

bot.run('API TOKEN')
