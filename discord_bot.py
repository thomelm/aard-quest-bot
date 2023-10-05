import discord
import telnetlib
import time
import asyncio
from config import credentials
from discord_webhook import DiscordWebhook

url = credentials['discord_webhook']
api_key = credentials['discord_api_key']

def get_level(tn):
     tn.write('level\n'.encode('ascii'))
     tn.read_until('You are level'.encode('ascii')).decode('ascii')
     char_level = tn.read_until('.'.encode('ascii')).decode('ascii')
     char_level = char_level.split(' ')[-1]
     char_level = char_level.split('.')[0]
     return int(char_level)

def get_gqs_comp(tn):
    tn.write('whois\n'.encode('ascii'))
    tn.read_until('Gquests Won:'.encode('ascii')).decode('ascii')
    gqs_comp = tn.read_until(']'.encode('ascii')).decode('ascii')
    gqs_comp = gqs_comp.split('     ')[-1]
    gqs_comp = gqs_comp.split('\x1b')[0]
    return int(gqs_comp)

def gquest(level, tn):
    tn.read_very_eager()
    tn.write('gq list\n'.encode('ascii'))
    tn.read_until('Num'.encode('ascii'))
    # gq_list = tn.read_until('] >'.encode('ascii')).decode('ascii').split('\x1b')
    gq_list = tn.read_until('] >'.encode('ascii')).decode('ascii').split('\x1b')
    gq_list = [item for item in gq_list if '***' not in item and '-----' not in item and 'Type' not in item][0]
    if type(gq_list) == list:
        gq_list = [item.split('\n\r\n\r')[0] for item in gq_list]
        gq_list = [item.split('m\n\r')[-1] for item in gq_list]
        print('is-list')
    else:
        gq_list = gq_list.split('\n\r')
        gq_list = [item for item in gq_list if len(item) > 6 and ('[' not in item or '] >' not in item)]
    print(gq_list)
    if len(gq_list) > 1:
        for x in range(0,len(gq_list)):
            quest_list = gq_list[x].split(' ')
            quest_list = [item for item in quest_list if item.isnumeric() or 'All' in item]
            if len(quest_list) > 4:
                min_lvl, max_lvl, q_num, wins = quest_list[2], quest_list[3], quest_list[0], quest_list[1]
                if int(min_lvl) <= level <= int(max_lvl):
                    return 1, q_num, wins
                elif x == len(gq_list) - 1:
                    return 0, 0, 0
    elif len(gq_list) == 1:
        quest_list = gq_list[0].split(' ')
        quest_list = [item for item in quest_list if item.isnumeric() or 'All' in item]
        if len(quest_list) > 4:
            min_lvl, max_lvl, q_num, wins = quest_list[2], quest_list[3], quest_list[0], quest_list[1]
            if int(min_lvl) <= level <= int(max_lvl):
                return 1, q_num, wins
            else:
                return 0, 0, 0
    else:
        return 0, 0, 0

async def telnet_waiting():
    webhook = DiscordWebhook(url=url, content="You can now quest again!")
    username = credentials['username']
    password = credentials['password']
    tn = telnetlib.Telnet('aardwolf.org', 23, 15)
    time.sleep(1)
    tn.read_very_eager()
    tn.write((username + '\n' + password + '\n\n').encode('ascii'))
    time.sleep(1)
    tn.read_very_eager()
    tn.write('\n'.encode('ascii'))
    time.sleep(1)
    x = tn.read_until('qt'.encode('ascii')).decode('ascii').split()[-1][0]
    qt = x[-1][0]  # x[3][0]
    time.sleep(1)
    level = get_level(tn)
    gquest_wins = get_gqs_comp(tn)
    gquest_list = []
    while True:
        tn.read_very_eager()
        tn.write('\n'.encode('ascii'))
        time.sleep(0.2)
        y = tn.read_until('qt'.encode('ascii')).decode('ascii').split()[-1][0]
        if (y != qt and int(y) == 0) or int(qt) == 0:
            print(y, qt, 'try again!')
            qt = y
            break
        else:
            tn.write('spellup\n'.encode('ascii'))
            print('keep waiting', y, qt)
        gquest_bool, gquest_value, wins = gquest(level, tn)
        print(gquest_bool, gquest_value, wins)
        if gquest_bool == 1 and gquest_value not in gquest_list and ((wins.isnumeric() and int(wins) > gquest_wins) or wins == 'All'):
            gquest_list.append(gquest_value)
            gq_webhoook = DiscordWebhook(url=url, content=f"GQuest {gquest_value} is available for your level!")
            gq_webhoook.execute()
        await asyncio.sleep(60)
    tn.close()
    webhook.execute()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.name == 'aardwolf-notifications' and message.author.name == 'floppybiscuits' and message.content.strip().upper() == 'QUEST':
            await message.channel.send('Starting Quest Idling Script')
            await telnet_waiting()

if __name__ == '__main__':
    client.run(api_key)
