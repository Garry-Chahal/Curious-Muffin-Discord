import discord
import os
import requests
import json
import random
import time
import asyncio
import dbl
import pytz
import gspread
import urllib
from datetime import datetime
from keep_alive import keep_alive
from google_trans_new import google_translator
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from oauth2client.service_account import ServiceAccountCredentials

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def get_prefix(guild_id):
    prefix_file = open('command_prefix.txt')
    prefix_file.seek(0) 
    for line in prefix_file.readlines():
        line = line.split(',')
        if(line[0] == str(guild_id)):
            return str(line[1]).strip()
    return '.'

def get_advice():
  response = requests.get("https://api.adviceslip.com/advice")
  json_data = json.loads(response.text)
  return json_data["slip"]["advice"]

def get_trivia():
  response = requests.get("https://useless-facts.sameerkumar.website/api")
  json_data = json.loads(response.text)
  return json_data["data"]

def get_numfact(input_number):
  response = requests.get("http://numbersapi.com/{number}?json".format(number = input_number))
  json_data = json.loads(response.text)
  return json_data["text"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']
  return quote

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/jokes/random")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + "\n" + json_data['punchline']
  return joke

def get_definition(input_word):
  try:
    response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/{word}".format(word = input_word))
    json_data = json.loads(response.text)
    word = json_data[0]["word"].capitalize()
    part_of_speech = json_data[0]["meanings"][0]["partOfSpeech"].capitalize()
    meanings = json_data[0]["meanings"][0]["definitions"][0]["definition"]
    data = "**Word:** " + word + "\n" + "**Part of Speech:** " + part_of_speech + "\n" + "**Definition:** " + meanings
    return ">>> " + data
  except:
    return "Sorry, I could not obtain the word definition at this time."

def get_news(news_source):
  try:
    chosen_news_api_key = "NEWS"+str(random.randrange(1,4))
    news_api_key = os.getenv(chosen_news_api_key)
    response = requests.get("http://newsapi.org/v2/top-headlines?sources={source}&apiKey={news_key}".format(source = news_source, news_key = news_api_key))
    json_data = json.loads(response.text)
    
    first_news = json_data["articles"][0]["description"]
    first_url = json_data["articles"][0]["url"]
    
    second_news = json_data["articles"][1]["description"]
    second_url = json_data["articles"][1]["url"]
    
    third_news = json_data["articles"][2]["description"]
    third_url = json_data["articles"][2]["url"]
    
    fourth_news = json_data["articles"][3]["description"]
    fourth_url = json_data["articles"][3]["url"]
    
    fifth_news = json_data["articles"][4]["description"]
    fifth_url = json_data["articles"][4]["url"]
  
    news_data = "**1.** " + first_news + "\n\t**Read more: **" + first_url + "\n\n**2.** " + second_news + "\n\t**Read more: **" + second_url + "\n\n**3.** " + third_news + "\n\t**Read more: **" + third_url + "\n\n**4.** " + fourth_news + "\n\t**Read more: **" + fourth_url + "\n\n**5.** " + fifth_news + "\n\t**Read more: **" + fifth_url
    return news_data
  except:
    return "We could not obtain any updated news stories this time."

def weather(location):
  try:
    weather_api_key = os.getenv('WEATHER1')
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key={weather_key}&q={link}&days=1".format(link = location, weather_key = weather_api_key))
    json_data = json.loads(response.text)
    location = ":earth_americas: **Location:** " + json_data["location"]["name"] + ", " + json_data["location"]["region"] + ", " + json_data["location"]["country"]
    local_time = json_data["location"]["localtime"]
    local_time =  datetime.strptime(local_time, '%Y-%m-%d %H:%M')
    local_time = "\n\n:alarm_clock: **Current Date and Time:** " + local_time.strftime("%b. %d, %Y @ %I:%M %p")
    temperature = "\n\n:partly_sunny: **Temperature:** " + str(json_data["current"]["temp_c"]) + "°C"
    feels_like = "\n\n:cloud_snow: **Feels Like:** " + str(json_data["current"]["feelslike_c"]) + "°C"
    condition = "\n\n:thunder_cloud_rain: **Conditions:** " + json_data["current"]["condition"]["text"]
    wind_speed = "\n\n:dash: **Wind Speed:** " + str(json_data["current"]["wind_kph"]) + " km/hr " + str(json_data["current"]["wind_dir"])
    visibility = "\n\n:eyes: **Visibility:** " + str(json_data["current"]["vis_km"]) + " km"
    uv_index = "\n\n:island: **UV Index:** " + str(json_data["current"]["uv"])
    sunrise = "\n\n:last_quarter_moon_with_face: **Sunrise:** " + json_data["forecast"]["forecastday"][0]["astro"]["sunrise"]
    sunset = "\n\n:last_quarter_moon_with_face: **Sunset:** " + json_data["forecast"]["forecastday"][0]["astro"]["sunset"]
    
    return location + local_time + temperature + feels_like + condition + wind_speed + visibility + uv_index + sunrise + sunset

  except:
    return "We could not obtain weather information at this time."

def clock(location):
  try:
    weather_api_key = os.getenv('WEATHER1')
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key={weather_key}&q={link}&days=1".format(link = location, weather_key = weather_api_key))
    json_data = json.loads(response.text)
    location = "**Location:** " + json_data["location"]["name"] + ", " + json_data["location"]["region"] + ", " + json_data["location"]["country"]
    local_time = json_data["location"]["localtime"]
    local_time =  datetime.strptime(local_time, '%Y-%m-%d %H:%M')
    local_time = "\n**Current Date and Time:** " + local_time.strftime("%b. %d, %Y @ %I:%M %p")
    
    return location + local_time
  except:
    return "We could not obtain time information at this time."

def stock(company):
  try:
    chosen_stock_api_key="STOCK"+str(random.randrange(1,4))
    stock_api_key = os.getenv(chosen_stock_api_key)
    response = requests.get("https://financialmodelingprep.com/api/v3/profile/{company_name}?apikey={stock_key}".format(company_name = company, stock_key = stock_api_key))
    json_data = json.loads(response.text)
    company_name = "Company Name: " + str(json_data[0]["companyName"])
    company_website = "\nCompany Website: " + str(json_data[0]["website"])
    company_ceo = "\nCompany CEO: " + str(json_data[0]["ceo"])
    company_employees = "\nCompany Employees: " + str(json_data[0]["fullTimeEmployees"])
    company_symbol = "\n\nStock Symbol: " + str(json_data[0]["symbol"])
    company_price = "\nStock Price: " + str(json_data[0]["price"])
    company_beta = "\nStock Beta: " + str(json_data[0]["beta"])
    company_changes = "\nStock Change: " + str(json_data[0]["changes"])
    company_currency = "\nStock Currency: " + str(json_data[0]["currency"])
    company_exchange = "\nStock Exchange: " + str(json_data[0]["exchangeShortName"])

    return company_name + company_website + company_ceo + company_employees + company_symbol + company_price + company_beta + company_changes + company_currency + company_exchange
  except:
    return "Please provide a valid stock symbol. For example, AAPL (Apple, Inc)"

def shorten_url(user_url):
	try:
		cuttly_api_key = os.getenv('CUTTLY')
		user_url = urllib.parse.quote(user_url)
		shortened_url = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(cuttly_api_key, user_url))
		json_data = json.loads(shortened_url.text)

		if json_data["url"]["status"] == 7:
			return (json_data["url"]["shortLink"])
		else:
			return "Sorry, the link you provided is invalid."
	except:
		return "Sorry, the link you provided is invalid."

def prefix_information(prefix, author):
  return f"""

  A **prefix** is the start of a message that I can recognize as my command.
  In the case of `.help` - `.` is the prefix and `help` is the command.

  If you're running more than one bot, you likely wouldn't want us both to respond to the same prefix.

  **Default Prefix:** `.`
  **Current Setting:** `{prefix}`
  **Examples:** `!` `?` `$` `#`

  You can also use letters, numbers, or characters as a prefix.
  At this time, `,` and `/` are not available as prefixes.

  If you forget your prefix, you will need to contact support.
  https://www.curiousmuffin.ml/contact

  **So, what __prefix__ would you like to use, {author}?**

  Please provide a prefix in the next 30 seconds.
  Type `000` to cancel and keep the same prefix.

  """

def list_news_sources(prefix):
  return f"""

  Good to know you're interested! You can access alternate news sources:

  • Canada (can)
  • Australia (aus)
  • United Kingdom (uk)
  • Technology (tech)
  • Sports (sport)
  • Gaming (game)

  By default, I show news stories from the United States `{prefix}news`. 
  Provide an option from above to get more specific news.

  **Use the format with a comma:**

  `{prefix}news, your choice`

  For example: `{prefix}news, tech`

  """

def math_operations_list(prefix):
  return f"""

  • **Addition (`Add`):** Add the 1st number by the 2nd number
  • **Subtraction (`Sub`):** Subtract the 1st number by the 2nd number
  • **Multiplication (`Multi`):** Multiply the 1st number by the 2nd number
  • **Division (`Div`):** Divide the 1st number by the 2nd number
  • **Exponentiation (`Expo`):** 1st number raised to the 2nd number
  • **Root (`Root`):** 1st number (index), 2nd number (radicand under root)
  • **Sum of Range (`Sum`):** Sum of values between the 1st and 2nd number (inclusive)
  • **Remainder (`Remain`):** Remainder of the 1st number divided by the 2nd number
  • **Mean Average (`Average`):** Average of the 1st and 2nd number

  __**Helpful Tip**__: 

  You can perform multiple operations on the same numbers!

  **Example:** `{prefix}math,add sub div, 5, 10`

  **Result:**
  ```\n15.0\n-5.0\n0.5\n```
  Curious Muffin will perform and provide the results in the given order.

  """

def tic_tac_toe(prefix):
  return f"""
  The first player to respond is X. 
  The second player to respond is O. 

  Both players take turns placing their marks on a 3 x 3 grid. 
  The first player to achieve 3 in a row (of his or her mark) wins. 
  The game is a tie if all 9 squares are full, and there is no winner.

  __**IMPORTANT:**__

  **Only ONE game can be played in a channel at a time!**

  Players must also choose a position within **30 seconds** on their turn.
  You can end the game at any time by providing an invalid position.

  To begin, type `{prefix}tictactoe`

  """

def rock_paper_scissors(prefix):
  return f"""

  Your choices are:

  • Rock (Rock wins against scissors)
  • Paper (Scissors win against paper)
  • Scissors (Paper wins against rock)

  The instant you make your selection, I will generate my move randomly.

  **To begin, use the format with a comma:**

  `{prefix}4game, your choice`

  For example: `{prefix}4game, rock`

  """

def save_information(prefix):
  return f"""
  I can store, retrieve, or remove textual information for you. 

  **IMPORTANT!**
  Please do not store confidential or private information.
  In other words, only store information that you would be comfortable with the public knowing.
  This may include content involving reminders, notes, or information about your server.

  For maximum protection, please create a strong password using letters, numbers, and symbols.

  To get started, choose a relevant option below. 
  **Store Information**        `{prefix}store`
  **Retrieve Information**     `{prefix}retrieve`
  **Remove Information**       `{prefix}remove`

  """

def retrieve_info(msg, prefix):
  retrieve_information = msg.strip().split("/")
  if len(retrieve_information) == 2:
    saved_information_file = open("information_storage.txt", "r")
    saved_information_file.seek(0)
    stored_password = str(retrieve_information[1]).strip()
    for line in saved_information_file:
      line_data = line.strip().split("/")
      if len(line_data) == 2:
        password = line_data[0]
        saved_data = line_data[1]
        if stored_password == password:
          return saved_data
    return "There is no information associated with that password."
  else:
    return(f">>> **Use the format with a slash:** `{prefix}retrieve/ your password`\n\nFor example: `{prefix}retrieve/password`")

def create_keyfile_dict():
  variables_keys = {
  "type": os.getenv("SHEET_TYPE"),
  "project_id": os.getenv("SHEET_PROJECT_ID"),
  "private_key_id": os.getenv("SHEET_PRIVATE_KEY_ID"),
  "private_key": os.getenv("SHEET_PRIVATE_KEY"),
  "client_email": os.getenv("SHEET_CLIENT_EMAIL"),
  "client_id": os.getenv("SHEET_CLIENT_ID"),
  "auth_uri": os.getenv("SHEET_AUTH_URI"),
  "token_uri": os.getenv("SHEET_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
  "client_x509_cert_url": os.getenv("SHEET_CLIENT_X509_CERT_URL")
  }
  return variables_keys

def server_commands_usage_log(guild_name, guild_id, command):
  date_format='%B %d, %Y'
  time_format='%-I:%M %p'

  current_date = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('US/Pacific')).strftime(date_format)
  current_time = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('US/Pacific')).strftime(time_format)

  commands_usage_row = [current_date, current_time, guild_name, guild_id, command]
  commands_usage_sheet.insert_row(commands_usage_row, 5)

  current_commands_count = int(server_information_sheet.cell(3,4).value)
  current_commands_count+=1
  server_information_sheet.update_cell(3, 4, current_commands_count)

def filterOnlyBots(member):
	return member.bot

game_options = {

"1game":"Guess the Number",
"2game":"Corny Jokes",
"3game":"Tic-Tac-Toe",
"4game":"Rock, Paper, Scissors"

}

greeting_response = [

  "Hey, how's it going?",
  "How has your day been?",
  "Nice to have you here!",
  "Let's talk!",
  "Since I just replied, am I now a human capable of communication?",
  "Let's all be grateful for having the opportunity to talk to one another. :smile:",
  "Hello mate. It's a beautiful day, isn't it?",
  "I don't need Hogwarts to be real, because you already bring the magic into my life.",
  "People say nothing is impossible, but I do nothing every day.",
  "Before someone criticizes me, I want to walk a mile in their shoes.\
  That way, I am a mile away from them and I have their shoes.",
  "I'm a perfectionist: a bot who wants to go from point A to point A+."

]

ask_me_responses = [

  "As I see it, yes.",
  "Ask again later.",
  "Better not tell you now.",
  "Cannot predict now.",
  "Concentrate and ask again.",
  "Don’t count on it.",
  "Maybe one day you'll be lucky enough to find out.",
  "Not so well, does that bother you?",
  "Shhh. . . it's too early to tell.",
  "All right so far, but there's still time for everything to go horribly wrong",
  "Thank you, next.",
  "Do you want an honest answer or the one you were expecting?",
  "It is certain.",
  "It is decidedly so.",
  "Chances aren't good.",
  "My sources said no, but they also said the Earth is flat.",
  "Yes. No. Maybe So.",
  "So, let’s take your doubts away.",
  "Brighten up your sight and use your own wisdom.",
  "Oh, so you now need help making decisions?",
  "Most likely.",
  "That's not my concern.",
  "Yes, if you leave me alone.",
  "My reply is no.",
  "My sources say no.",
  "Outlook not so good.",
  "I've got more important things to do than this.",
  "Outlook good.",
  "Reply hazy, try again.",
  "Signs point to yes.",
  "Very doubtful.",
  "Without a doubt.",
  "Yes.",
  "Yes – definitely.",
  "Everyone asks me their questions, but no one asks 'How are you, Muffin?'",
  "You may rely on it."
  
]

polite_responses = [
  "I'm well, just a bit tired from all the work...",
  "Good! I appreciate you asking.",
  "I can’t complain, but sometimes I still do.",
  "Oh, you know, every day is better than the next.",
  "Better than some, not as good as others.",
  "Somewhere between better and best.",
  "All the better now that you asked.",
  "I love you.",
  "If I were doing any better, I'd hire you to enjoy it with me.",
  "Overworked and underpaid.",
  "Everything is fine with you around.",
  "I’m single and ready to mingle!",
  "I could really go for a big, warm hug right now.",
  "Thank you for asking. You just made my day.",
  "If I was any finer, I'd be China",
  "Livin' the dream.",
  "Nice and dandy like cotton candy.",
  "If I had a tail, I would wag it."
]

welcome_message = """

Hello, **{}**! :wave: 

I'm Curious Muffin, and I'm here to help as your cheerful assistant.

Here are some things I can help around with:

• Deliver breaking news and weather information based on your interests
• Provide jokes, quotes, trivia, games, and life advice
• Provide definitions, solve math, and keep track of the time
• Store important textual information

Type `.help` to see everything I can do!
You can change the command prefix at any time.

Join the Curious Muffin Discord Server!
Access the latest announcements, giveaways, request features, and more!

https://dsc.gg/curious-muffin

"""

welcome_direct_message = """

Hello! :wave:

I'm Curious Muffin, and I'm here to help as your server's cheerful assistant. 

Type `.help` in your server to see what I can do.
You can change the command prefix at any time.

Join the Curious Muffin Discord Server!
Access the latest announcements, giveaways, request features, and more!

https://dsc.gg/curious-muffin

Thanks for the invite!

"""

change_log = """
**Version 1.5 changelog (February 24, 2021)**
• Improved format and design for .vote and .embed commands
• Vote and Embed "Commands" are automatically deleted

**Version 1.4 changelog (February 20, 2021)**
• Translate any given text to any language with .translate
• Get detailed information about any user with .user
• Check Curious Muffin's response time with .ping
• Create your own embeds for any message! Use .embed

**Version 1.3 changelog (February 18, 2021)**

• Curious Muffin is now officially verified by Discord!
• UI changes for the .help command
• Access stock information with .stock
• Access the world clock with .clock
• Access your server information with .server
• Send feedback or bug reports directly using .feedback

**Version 1.2 changelog (February 10, 2021)**

• There's a new website redesign for Curious Muffin!
• Bug Fixes and Improvements.

**Version 1.1 changelog (January 9, 2021)**

• Change the command prefix of Curious Muffin
• Updated Profile Picture for Curious Muffin
• Tic-Tac-Toe should be much more responsive!

**Version 1.0 changelog (January 8, 2021)**

• Initial Public release of Curious Muffin
• Randomly select a server member (.random)
• Bug Fixes and Improvements

**Version 0.0 changelog (December 25, 2020)**

• Initial beta (private) release of Curious Muffin

Thank you for your support! All feedback is appreciated.

"""

translatable_languages = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese1': 'zh-cn', 'chinese2': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish': 'ku', 'kurmanji': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'mandarin': 'zh-cn', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar': 'my', 'burmese': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'turkmen': 'tk', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}

all_available_commands = ["fun", "hi", "ask", "advice", "quote", "joke", "fact", "numfact", "info", "news", "weather", "clock", "stock", "server", "game", "1game", "2game", "tictactoe", "3game", "4game", "random", "coin", "dice", "rng", "choose", "member", "utility", "word", "math", "time", "vote", "save", "store", "retrieve", "remove", "dev", "updates", "prefix", "feedback", "help", "translate", "user", "ping", "embed", "poll", "sendf", "avatar", "link"]

help_command_links = """
[Invite Me](https://discord.com/api/oauth2/authorize?client_id=790985487107620865&permissions=93376&scope=bot) - [Discord Server](https://discord.gg/ZvZmTUnWng) - [Vote for Me](https://top.gg/bot/790985487107620865)
"""
discord_server_invite = """
[http://dsc.gg/curious-muffin](http://dsc.gg/curious-muffin)
"""

top_gg = os.getenv('TOP_GG')
client.dblpy = dbl.DBLClient(client, top_gg, autopost=True)

scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

google_creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scope)
google_client = gspread.authorize(google_creds)

server_information_sheet = google_client.open("Curious Muffin Database").worksheet("Server Information")
commands_usage_sheet = google_client.open("Curious Muffin Database").worksheet("Server Commands Usage")
server_feedback_sheet = google_client.open("Curious Muffin Database").worksheet("Server Feedback")
information_storage_sheet = google_client.open("Curious Muffin Database").worksheet("Information Storage")
command_prefix_sheet = google_client.open("Curious Muffin Database").worksheet("Command Prefix")

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@client.event
async def on_guild_join(guild):
  for general in guild.text_channels:
    if general and general.permissions_for(guild.me).send_messages:
      await general.send(welcome_message.format(guild.name))
      break

  def check(event):
      return event.target.id == client.user.id

  try:
    bot_invite = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
    await bot_invite.user.send(welcome_direct_message)
  except:
    pass

@client.event
async def on_guild_remove(guild):
  prefix_file = open('command_prefix.txt', 'r+')
  read_only_prefix_file = prefix_file.read()
  prefix_file.seek(0)
  for line in read_only_prefix_file.split("\n"):
    line_data = line.strip().split(",")
    if len(line_data) == 2:
      guild_id = str(line_data[0]).strip()
      if guild_id != str(guild.id).strip():
        prefix_file.write(line + "\n")
  prefix_file.truncate()
  prefix_file.close()

@client.event
async def on_ready():
  print('The Discord Bot is currently logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game('.help to begin'))

  update_sheet = 1
  if update_sheet == 1:

    server_names = ""
    server_ids = ""
    server_owner = ""
    server_member_count = ""
    total_users = 0
    for guild in client.guilds:
      server_names += str(guild.name) + '\n'
      server_ids += str(guild.id) + '\n'
      server_owner += str(guild.owner) + '\n'
      server_member_count += "Members: " + str(len(guild.members)) + '\n'
      total_users += int(len(guild.members))

    server_information_sheet.update_cell(5, 1, server_names)
    server_information_sheet.update_cell(5, 2, server_ids)
    server_information_sheet.update_cell(5, 3, server_member_count)
    server_information_sheet.update_cell(5, 4, server_owner)
    server_information_sheet.update_cell(1,4, len(client.guilds))

    # user_statistics_channel = client.get_channel(821986752364281866)
    # await user_statistics_channel.edit(name='{}+ Users'.format(int(total_users)))

    print("Server Statistics Collected.")
  else:
    print("Server Statistics Not Collected.")

@client.event
async def on_message(message):
	msg = message.content
	msgc = message.channel.send

	if message.author == client.user: return

	if message.author.bot: return

	if message.guild is None and message.author.bot == False:
		await message.author.send(welcome_direct_message)
		return

	if message == None or message.guild == None: return
		
	prefix = get_prefix(message.guild.id)

  # if "discord.gg" in msg and message.guild.id == 814294614165028866:
  #   if "https://discord.gg/ZvZmTUnWng" not in msg:
  #     author = message.author.name
  #     if message.channel.permissions_for(message.guild.me).send_messages:
  #         if not(message.author.guild_permissions.manage_guild or message.author.guild_permissions.manage_roles):
  #           await message.delete()
  #           await msgc(f">>> **Sorry {author} - You cannot post that link here!**")

	if msg.startswith(prefix) and message.channel.permissions_for(message.guild.me).send_messages:

		if msg.startswith(prefix + 'fun'):
			embed=discord.Embed(title="Fun Commands", color=discord.Colour.teal())
			
			embed.add_field(name=f"`{prefix}hi`", value="Chat with me", inline=False)
			embed.add_field(name=f"`{prefix}ask`", value="Ask me anything (Magic 8-ball)", inline=False)
			embed.add_field(name=f"`{prefix}advice`", value="Receive motivational advice", inline=False)
			embed.add_field(name=f"`{prefix}quote`", value="Receive motivational quotes", inline=False)
			embed.add_field(name=f"`{prefix}joke`", value="See a random joke", inline=False)
			embed.add_field(name=f"`{prefix}fact`", value="See a random trivia fact", inline=False)
			embed.add_field(name=f"`{prefix}numfact`", value="See a number fact", inline=False)
			embed.add_field(name=f"`{prefix}sendf`", value="Send F to pay respect", inline=False)
			await msgc(embed=embed)

		if msg.startswith(prefix + 'hi'):
			await msgc(random.choice(greeting_response))

		if msg.startswith(prefix + 'ask'):
			list_of_questions = msg.split("ask,")
			if len(list_of_questions) > 1:
				user_asking_message = str(list_of_questions[1]).strip().lower()
				if user_asking_message.startswith("how are you") or "muffin" in user_asking_message:
					await msgc(random.choice(polite_responses))
				else:
					await msgc(random.choice(ask_me_responses))
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}ask, question`\n\nFor example: `{prefix}ask, Is this the real life?`")

		if msg.startswith(prefix + 'advice'):
			await msgc(get_advice())

		if msg.startswith(prefix + 'quote'):
			await msgc(get_quote())
		
		if msg.startswith(prefix + 'joke'):
			await msgc(get_joke())
			
		if msg.startswith(prefix + 'fact'):
			await msgc(get_trivia())

		if msg.startswith(prefix + 'numfact'):
			list_of_number = msg.split(",")
			if len(list_of_number) == 2:
				try:
					number = str(list_of_number[1]).strip()
					await msgc(get_numfact(number))
				except:
					await msgc("Sorry, you did not provide a valid number.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}numfact, number`\n\nFor example: `{prefix}numfact, 98`")

		if msg.startswith(prefix + 'sendf'):
			f_emoji_value = "<:f_key:822280865044103168>"
			f_emoji = (f"{f_emoji_value} {f_emoji_value} {f_emoji_value} {f_emoji_value}\n"
								f"{f_emoji_value}\n"
								f"{f_emoji_value} {f_emoji_value} {f_emoji_value}\n"
								f"{f_emoji_value}\n"
								f"{f_emoji_value}\n")
			await msgc(f_emoji)

		if msg.startswith(prefix + 'info'):
			embed=discord.Embed(title="Information Commands", color=discord.Colour.red())
			
			embed.add_field(name=f"`{prefix}news`", value="Access interest-based news", inline=False)
			embed.add_field(name=f"`{prefix}weather`", value="Access weather information", inline=False)
			embed.add_field(name=f"`{prefix}clock`", value="Access world clock information", inline=False)
			embed.add_field(name=f"`{prefix}stock`", value="Access stock and company information", inline=False)
			embed.add_field(name=f"`{prefix}server`", value="Access your server statistics", inline=False)
			embed.add_field(name=f"`{prefix}user`", value="Access information about any user", inline=False)
			embed.add_field(name=f"`{prefix}avatar`", value="Preview and receive a link to a user's avatar", inline=False)
			await msgc(embed=embed)

		if msg.startswith(prefix + 'news'):
			author = message.author
			await msgc(':newspaper:  **Here is the latest news, {}.**'.format(author))

			list_of_news = msg.split(",")
			if len(list_of_news) == 2:
				user_news = str(list_of_news[1]).strip().lower()

				if user_news == "canada" or user_news == "can":
					news_source = "google-news-ca"
				
				elif user_news == "australia" or user_news == "aus":
					news_source = "abc-news-au"

				elif user_news == "uk" or user_news == "united kingdom":
					news_source = "google-news-uk"

				elif user_news == "tech" or user_news == "technology":
					news_source = "the-verge"      

				elif user_news == "sport" or user_news == "sports":
					news_source = "espn"      

				elif user_news == "game" or user_news == "gaming":
					news_source = "polygon"        
				
				else:
					news_source = "google-news"

				embed=discord.Embed(color=discord.Colour.red())     
				embed.description = get_news(news_source)
				await msgc(embed=embed)

			else:
				embed=discord.Embed(color=discord.Colour.red())

				embed.description = get_news("google-news")
				await msgc(embed=embed)

				await msgc(f"> Psst... if you want to see everything you can do with `{prefix}news`, type `reveal` in the next 30 seconds.")
				
				channel = message.channel
				def check(news_help_interest):
					return (news_help_interest.content).strip().lower() == 'reveal' and news_help_interest.channel == channel
				try:
					await client.wait_for('message', timeout=30.0, check=check)
				except asyncio.TimeoutError:
					return
				else:
					embed=discord.Embed(color=discord.Colour.blurple())
					embed.description = list_news_sources(prefix)
					await msgc(embed=embed)

		if msg.startswith(prefix + 'weather'):
			list_of_weather = msg.split(",")
			if len(list_of_weather) == 2:
				user_location = str(list_of_weather[1]).strip().lower()
				embed=discord.Embed(title = "Weather Information", color=discord.Colour.blurple())
				embed.description = weather(user_location)
				await msgc(embed=embed)
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}weather, location`\n\nFor example: `{prefix}weather, Los Angeles`")

		if msg.startswith(prefix + 'clock'):
			list_of_time = msg.split(",")
			if len(list_of_time) == 2:
				user_location = str(list_of_time[1]).strip().lower()
				await msgc(clock(user_location))
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}clock, location`\n\nFor example: `{prefix}clock, Los Angeles`")

		if msg.startswith(prefix + 'stock'):
			list_of_stock = msg.split(",")
			if len(list_of_stock) == 2:
				user_company = str(list_of_stock[1]).strip().lower()
				embed=discord.Embed(title = "Stock Information", color=discord.Colour.gold())
				embed.description = stock(user_company)
				embed.set_thumbnail(url="https://i.imgur.com/pdNIpNB.png")
				await msgc(embed=embed)
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}stock, company symbol`\n\nFor example: `{prefix}stock, AAPL`")

		if msg.startswith(prefix + 'server'):
			server_name = str(message.guild.name)
			server_owner = str(message.guild.owner)
			server_id = str(message.guild.id)
			server_created = str(message.guild.created_at.strftime("%b. %d, %Y @ %I:%M %p"))
			server_member_count = message.guild.member_count
			server_bot_count = len(list(filter(filterOnlyBots, message.guild.members)))
			server_user_count = str(server_member_count - server_bot_count)
			server_icon = str(message.guild.icon_url)
			server_icon_link = shorten_url(server_icon)

			embed=discord.Embed(title = "__Server Information__", color=discord.Colour.blue())
			embed.description = "Server Name: " + server_name + "\nServer Admin: " + server_owner + "\nServer ID: " + server_id + \
			"\nServer Creation Date (UTC): " + server_created + "\nServer Total Member Count: " + str(server_member_count) + "\nServer User Count: " + server_user_count + "\nServer Bot Count: " + str(server_bot_count) + "\nServer Icon Link: " + server_icon_link
			embed.set_thumbnail(url = server_icon)
			await msgc(embed=embed)

		if msg.startswith(prefix + 'user'):
			list_of_user = msg.split(",")
			if len(list_of_user) == 2:
				user_guild_from_message = message.guild.id
				user_guild = client.get_guild(user_guild_from_message)

				user_id_as_string = str(list_of_user[1]).strip(" <!@>")

				if user_id_as_string.isdigit():
					user_id_as_int = int(user_id_as_string)
					if user_guild.get_member(user_id_as_int) is not None:
						username = user_guild.get_member(user_id_as_int)
						user_id = "\nMember ID: " + str(user_id_as_int)
						user_guild = "\nMember Guild: " + str(user_guild)
						user_member_verification = "\nPending Verification: " + str(username.pending)
						user_member_premium = "\nNitro Boost Active (UTC): " + str(username.premium_since)
						user_top_role = "\nTop Server Role: " + str(username.top_role)
						user_created_at = "\nAccount Creation Date (UTC): " + str(username.created_at.strftime("%b. %d %Y, %I:%M %p"))
						user_joined_at = "\nServer Join Date (UTC): " +  str(username.joined_at.strftime("%b. %d %Y, %I:%M %p"))
						user_icon = str(username.avatar_url)
						user_icon_link = "\nUser Avatar Link: " + shorten_url(user_icon)

						embed=discord.Embed(title = "__User Information__", color=discord.Colour.purple())
						embed.description = "Member Username: " + str(username) + user_id + user_guild + \
						user_member_verification + user_member_premium + user_top_role + user_created_at + user_joined_at + user_icon_link

						embed.set_thumbnail(url = username.avatar_url)

						await msgc(embed=embed)
					else:
						try:
								await client.fetch_user(user_id_as_int)
								username = await client.fetch_user(user_id_as_int)
								user_id = "\nMember ID: " + str(user_id_as_int)
								user_created_at = "\nAccount Creation Date (UTC): " + str(username.created_at.strftime("%b. %d %Y, %I:%M %p"))
								user_icon = str(username.avatar_url)
								user_icon_link = "\nUser Avatar Link: " + shorten_url(user_icon)

								embed=discord.Embed(title = "__User Information__", color=discord.Colour.purple())
								embed.description = "Member Username: " + str(username) + user_id + user_created_at + user_icon_link

								embed.set_thumbnail(url = username.avatar_url)

								await msgc(embed=embed)
						except:
								await msgc("The username or ID you provided does not match any current user.")
				else:
					await msgc("I could not obtain information for that user at this time.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}user, username or user ID`\n\nFor example: `{prefix}user, @Curious Muffin` or `{prefix}user, 790985487107620865`")

		if msg.startswith(prefix + 'avatar'):
			list_of_user = msg.split(",")
			if len(list_of_user) == 2:
				user_guild_from_message = message.guild.id
				user_guild = client.get_guild(user_guild_from_message)

				user_id_as_string = str(list_of_user[1]).strip(" <!@>")

				if user_id_as_string.isdigit():
					user_id_as_int = int(user_id_as_string)
					if user_guild.get_member(user_id_as_int) is not None:
						username = user_guild.get_member(user_id_as_int)
						user_icon = str(username.avatar_url)
						user_icon_link = "\nUser Avatar Link: " + shorten_url(user_icon)

						embed=discord.Embed(title = "__{}'s Avatar__".format(str(username)), color=discord.Colour.red())
						embed.description = user_icon_link

						embed.set_image(url = username.avatar_url)

						await msgc(embed=embed)
					else:
						try:
								await client.fetch_user(user_id_as_int)
								username = await client.fetch_user(user_id_as_int)
								user_icon = str(username.avatar_url)
								user_icon_link = "\nUser Avatar Link: " + shorten_url(user_icon)

								embed=discord.Embed(title = "__{}'s Avatar__".format(str(username)), color=discord.Colour.red())
								embed.description = user_icon_link

								embed.set_image(url = username.avatar_url)

								await msgc(embed=embed)
						except:
								await msgc("The username or ID you provided does not match any current user.")
				else:
					await msgc("I could not obtain the avatar for that user at this time.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}avatar, username or user ID`\n\nFor example: `{prefix}avatar, @Curious Muffin` or `{prefix}avatar, 790985487107620865`")

		if msg.startswith(prefix + 'game'):
			author = message.author
			embed=discord.Embed(
				title="Game Commands", color=discord.Colour.gold())

			embed.description = "Let's get started, {}!".format(author)

			for (game_command,game_description) in game_options.items():
				embed.add_field(name="`"+ prefix + game_command +"`", value=game_description, inline=False)

			await msgc(embed=embed)

		if msg.startswith(prefix + '1game'):
			secret_number = random.choice(range(1,101))
			embed=discord.Embed(
				title="**Please guess a number between 1-100!**", color=discord.Colour.blue())

			embed.description = 'There are only 6 tries and anyone can guess.\nType "0" to end the game'

			await msgc(embed=embed)
			channel = message.channel
			number_game_range_options = list(map(str, range(0,101)))

			def check(number_game_response):
				return str(number_game_response.content).strip() in number_game_range_options and number_game_response.channel == channel

			try:
				message_response = await client.wait_for('message', timeout=30.0, check=check)

			except asyncio.TimeoutError:
				await channel.send("> It's been more than 30 seconds. I chose **" + str(secret_number) + ".**")
				return

			else:
				guess = int(message_response.content)
				guesses_left = 5

				while guess != secret_number and guesses_left > 0 and guess != 0:
					if guess == 0:
						guesses_left = 0

					elif guess < secret_number:
						embed=discord.Embed(title="**Higher! Try again.**", color=discord.Colour.magenta())

						embed.description = 'Type "0" to end the game.\nRange: 1-100\n__**Guesses left:**__ '+ str(guesses_left)

						await msgc(embed=embed)
						def check(number_game_response):
							return str(number_game_response.content).strip() in number_game_range_options and number_game_response.channel == channel

						try:
							message_response = await client.wait_for('message', timeout=30.0, check=check)

						except asyncio.TimeoutError:
							await channel.send("> It's been more than 30 seconds. I chose **" + str(secret_number) + ".**")
							return

						else:
							guess = int(message_response.content)

					elif guess > secret_number:
						embed=discord.Embed(title="**Lower! Try again.**", color=discord.Colour.magenta())

						embed.description = 'Type "0" to end the game.\nRange: 1-100\n__**Guesses left:**__ '+ str(guesses_left)

						await msgc(embed=embed)
						def check(number_game_response):
							return str(number_game_response.content).strip() in number_game_range_options and number_game_response.channel == channel

						try:
							message_response = await client.wait_for('message', timeout=30.0, check=check)

						except asyncio.TimeoutError:
							await channel.send("> It's been more than 30 seconds. I chose **" + str(secret_number) + ".**")
							return

						else:
							guess = int(message_response.content)
					guesses_left -= 1

				if guess == secret_number:
					await msgc("Yes, that is correct. I chose " + str(secret_number) + " :v: ")
				else:
					await msgc("Sorry, the chosen number was " + str(secret_number) + ".")

		if msg.startswith(prefix + '2game'): 
			channel = message.channel
			cornyjokesfile = open("cornyjokes.txt")
			corny_jokes = {}
			for line in cornyjokesfile:
				(number,joke_question,joke_response) = line.strip().split("/")
				corny_jokes[joke_question] = joke_response
			cornyjokesfile.close()

			continue_jokes = True
			round = 1
			while continue_jokes:
				embed=discord.Embed(title="**Round: **" + str(round), color=discord.Colour.green())

				embed.description = "When you're ready to continue, type '**START**'."

				await msgc(embed=embed)

				def check(begin_joke):
					return (begin_joke.content).lower() == 'start' and begin_joke.channel == channel

				try:
					wait_for_response = await client.wait_for('message', timeout=120.0, check=check)
				except asyncio.TimeoutError:
					await channel.send("> Sorry, I've been waiting for too long. I'll take your leave for now.")
					continue_jokes = False
					return
				else:
					(joke,answer) = random.choice(list(corny_jokes.items()))

					embed=discord.Embed(title="Question: " + joke, color=discord.Colour.blurple())

					embed.description = "Type `DONE` to compare your responses.\
					\nType `STOP` to end the game.\n\nAll players must guess within 30 seconds!"

					await msgc(embed=embed)

					def check(view_answer):
						return (view_answer.content).upper() == 'DONE' or (view_answer.content).upper() == 'STOP' and view_answer.channel == channel
					try:
						wait_for_response = await client.wait_for('message', timeout=30.0, check=check)
					except asyncio.TimeoutError:
						embed=discord.Embed(title="Sorry, the time is up!", color=discord.Colour.blurple())

						embed.description = "**Joke:** " + joke + "\n**Response:** " + answer + f"\n\nType `{prefix}game` to view all available game options."

						await msgc(embed=embed)          
						continue_jokes = False
						return
					else:
						if str(wait_for_response.content).upper() == "STOP":
							await msgc("> For sure. We can play again later.")
							continue_jokes = False
						else:
							embed=discord.Embed(title="Game Result", color=discord.Colour.blurple())

							embed.description = "**Joke:** " + joke + "\n**Response:** " + answer

							await msgc(embed=embed)              
							round += 1
							await asyncio.sleep(5)
		
		if msg.startswith(prefix + 'tictactoe'):
			channel = message.channel
			embed=discord.Embed(title="Let's play Tic Tac Toe!", color=discord.Colour.green())
			embed.description = "Player 1: Respond with `X`."
			await msgc(embed=embed)  

			def check(tic_tac_toe_player1):
				return (tic_tac_toe_player1.content).strip().lower() == 'x' and tic_tac_toe_player1.channel == channel

			try:
				player1_response = await client.wait_for('message', timeout=30.0, check=check)

			except asyncio.TimeoutError:
				await channel.send(f">>> Sorry, I haven't heard from Player 1 yet.\nType `{prefix}game` to view all available game options again.")
				return

			else:
				player1 = player1_response.author.id
				embed=discord.Embed(title="Let's play Tic Tac Toe!", color=discord.Colour.red())
				embed.description = "Player 2: Respond with `O`."
				await msgc(embed=embed)

				def check(tic_tac_toe_player2):
					return (tic_tac_toe_player2.content).strip().lower() == 'o' and tic_tac_toe_player2.channel == channel

				try:
					player2_response = await client.wait_for('message', timeout=30.0, check=check)

				except asyncio.TimeoutError:
					await channel.send(f">>> Sorry, I haven't heard from Player 2 yet.\nType `{prefix}game` to view all available game options again.")
					return
				
				else:
					player2 = player2_response.author.id
					board = ["-", "-", "-",
									"-", "-", "-",
									"-", "-", "-"]

					continue_playing = True
					current_player = "X"
					current_playerid = player1

					await msgc(
					board[0] + " | " + board[1] + " | " + board[2] + "     1 | 2 | 3\n" + \
					board[3] + " | " + board[4] + " | " + board[5] + "     4 | 5 | 6\n" + \
					board[6] + " | " + board[7] + " | " + board[8] + "     7 | 8 | 9"
					)

					def check_for_winner():
						winner = ""

						row_winner = check_rows()
						column_winner = check_columns()
						diagonal_winner = check_diagonals()

						if row_winner:
							winner = row_winner
						elif column_winner:
							winner = column_winner
						elif diagonal_winner:
							winner = diagonal_winner
						
						return winner


					def check_rows():
						row_1 = board[0] == board[1] == board[2] != "-"
						row_2 = board[3] == board[4] == board[5] != "-"
						row_3 = board[6] == board[7] == board[8] != "-"

						if row_1:
							return board[0]
						elif row_2:
							return board[3]
						elif row_3:
							return board[6]

					def check_columns():
						column_1 = board[0] == board[3] == board[6] != "-"
						column_2 = board[1] == board[4] == board[7] != "-"
						column_3 = board[2] == board[5] == board[8] != "-"

						if column_1:
							return board[0] 
						elif column_2:
							return board[1] 
						elif column_3:
							return board[2] 

					def check_diagonals():
						diagonal_1 = board[0] == board[4] == board[8] != "-"
						diagonal_2 = board[2] == board[4] == board[6] != "-"

						if diagonal_1:
							return board[0] 
						elif diagonal_2:
							return board[2]

					scoreboard_filled = 0
					while continue_playing:
						await msgc("**" + current_player + "'s** turn.\nPlease choose a position from 1 to 9. ")

						def check(tic_tac_toe_player_turn):
							return (tic_tac_toe_player_turn.author.id) == current_playerid and tic_tac_toe_player_turn.channel == channel

						try:
							current_player_response = await client.wait_for('message', timeout=30.0, check=check)

						except asyncio.TimeoutError:
							await channel.send(">>> Sorry, I haven't heard back yet.\n**Game over.**")
							return
						
						else:
							position = str(current_player_response.content)
							valid_input = False

							while not valid_input:
								
								if str(position) not in ["1","2","3","4","5","6","7","8","9"]:
									await msgc("The position you provided was not between 1 and 9. **Game over.**")
									return
													
								position = int(position) - 1
								if board[position] == "-":
									valid_input = True

								else:
									await msgc("That position is already taken. Please try another position.")

									def check(tic_tac_toe_player_turn):
										return (tic_tac_toe_player_turn.author.id) == current_playerid and tic_tac_toe_player_turn.channel == channel

									try:
										current_player_response = await client.wait_for('message', timeout=30.0, check=check)

									except asyncio.TimeoutError:
										await channel.send(">>> Sorry, I haven't heard back yet.\n**Game over.**")
										return
									else:
										position = str(current_player_response.content)

						board[position] = current_player

						await msgc(
						board[0] + " | " + board[1] + " | " + board[2] + "     1 | 2 | 3\n" + \
						board[3] + " | " + board[4] + " | " + board[5] + "     4 | 5 | 6\n" + \
						board[6] + " | " + board[7] + " | " + board[8] + "     7 | 8 | 9"
						)

						winner = check_for_winner()
						scoreboard_filled += 1

						if current_player == "X":
							current_player = "O"
							current_playerid = player2

						elif current_player == "O":
							current_player = "X"
							current_playerid = player1          
						
						if winner == "X" or winner == "O":
							embed=discord.Embed(title="Game over! " + winner + " is the winner :clap: ", color=discord.Colour.blue())
							await msgc(embed=embed)             
							return

						if scoreboard_filled == 9:
							embed=discord.Embed(title="Game Over! It is a tie. :white_check_mark:", color=discord.Colour.blue())
							await msgc(embed=embed)               
							return

		if msg.startswith(prefix + '3game'):
			author = message.author
			embed=discord.Embed(title="Tic-Tac-Toe", color=discord.Colour.blue())
			embed.description = tic_tac_toe(prefix)
			await msgc(embed=embed)  

		if msg.startswith(prefix + '4game'):
			game_content = msg.split(",")
			if len(game_content) == 2:
				chosen_hand = str(game_content[1]).strip().lower().capitalize()
				rock_options = ["Rock", "Paper", "Scissors"]
				bot_option_chosen = random.choice(rock_options)
				await msgc("**You threw " + chosen_hand + ". I threw " + bot_option_chosen + ".**")

				if chosen_hand == bot_option_chosen:
					await msgc("Tie! :handshake: ")
				elif chosen_hand == "Rock":
					if bot_option_chosen == "Paper":
						await msgc("You lose! " + bot_option_chosen + " covers " + chosen_hand + " :yawning_face: ")
					else:
						await msgc("You win! " + chosen_hand + " smashes " + bot_option_chosen + " :clap: ")
				elif chosen_hand == "Paper":
					if bot_option_chosen == "Scissors":
						await msgc("You lose! " + bot_option_chosen + " cut " + chosen_hand + " :yawning_face: ")
					else:
						await msgc("You win! " + chosen_hand + " covers " + bot_option_chosen + " :clap: ")
				elif chosen_hand == "Scissors":
					if bot_option_chosen == "Rock":
						await msgc("You lose! " + bot_option_chosen + " smashes " + chosen_hand + " :yawning_face: ")
					else:
						await msgc("You win! " + chosen_hand + " cut " + bot_option_chosen + " :clap: ")
				else:
					await msgc(f">>> You did not provide a valid option.\n**Use the format with a comma:** `{prefix}4game, your choice`\n\nFor example: `{prefix}4game, rock`")
			else:
				embed=discord.Embed(title="Rock, Paper, Scissors", color=discord.Colour.magenta())

				embed.description = rock_paper_scissors(prefix)

				await msgc(embed=embed)     

		if msg.startswith(prefix + 'random'):
			embed=discord.Embed(
				title="Random Commands", color=discord.Colour.purple())
				
			embed.add_field(name=f"`{prefix}coin`", value="Flip a coin", inline=False)
			embed.add_field(name=f"`{prefix}dice`", value="Roll a die", inline=False)
			embed.add_field(name=f"`{prefix}rng`", value="Choose a random number out of a range", inline=False)
			embed.add_field(name=f"`{prefix}choose`", value="Choose a random item from your list", inline=False)
			embed.add_field(name=f"`{prefix}member`", value="Name a random member in your server", inline=False)

			await msgc(embed=embed)

		if msg.startswith(prefix + 'rng'):
			list_of_num = msg.split(",")
			if len(list_of_num) > 2:
				try:
					begin_range = list_of_num[1].strip()
					end_range = list_of_num[2].strip()
					await msgc(random.choice(range(int(begin_range),int(end_range)+1)))
				except:
					await msgc("Sorry, I am unable to compute a random number for that range.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}rng, starting number, last number`\n\nFor example: `{prefix}rng, 1, 100`")

		if msg.startswith(prefix + 'coin'):
			coin = ["heads","tails"]
			await msgc("> :coin: It's " + random.choice(coin))

		if msg.startswith(prefix + 'dice'):
			await msgc("> :game_die: I rolled a " + str(random.choice(range(1,7))))

		if msg.startswith(prefix + 'choose'):
			list_of_choices = msg.strip(" ,").split(",")
			if len(list_of_choices) > 1:
				await msgc(random.choice(list_of_choices[1:]))
			else:
				await msgc(f">>> **Separate the items with a comma:** `{prefix}choose, list of items`\n\nFor example: `{prefix}choose, Alex, Josh, Muffin, Dakota`")

		if msg.startswith(prefix + 'member'):
			guild_members_random = message.guild.members
			await msgc(random.choice(guild_members_random))

		if msg.startswith(prefix + 'utility'):
			embed=discord.Embed(
				title="Utility Commands", color=discord.Colour.red())
				
			embed.add_field(name=f"`{prefix}link`", value="Shorten a URL link", inline=False)
			embed.add_field(name=f"`{prefix}word`", value="Access word definitions", inline=False)
			embed.add_field(name=f"`{prefix}math`", value="Perform advanced math operations", inline=False)
			embed.add_field(name=f"`{prefix}translate`", value="Translate any text to another language", inline=False)
			embed.add_field(name=f"`{prefix}embed`", value="Display your text as an embed", inline=False)
			embed.add_field(name=f"`{prefix}time`", value="Start a stopwatch", inline=False)
			embed.add_field(name=f"`{prefix}vote`", value="Start a voting environment", inline=False)
			embed.add_field(name=f"`{prefix}poll`", value="Start a poll with up to 10 options", inline=False)
			embed.add_field(name=f"`{prefix}save`", value="Store, retrieve, or remove information", inline=False)

			await msgc(embed=embed)

		if msg.startswith(prefix + 'link'):
			user_link_command = msg.split(f"{prefix}link,")
			if len(user_link_command) == 2:
				user_url = str(user_link_command[1]).strip()
				await msgc("Here's your shortened link: " + shorten_url(user_url))
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}link, [link to shorten]`\n\nFor example: `{prefix}link, https://google.com`")

		if msg.startswith(prefix + 'word'):
			list_of_words = msg.split(",")
			if len(list_of_words) == 2:
				user_word = str(list_of_words[1]).strip()
				await msgc(get_definition(user_word))
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}word, word`\n\nFor example: `{prefix}word, Muffin`")
				
		if msg.startswith(prefix + 'math'):
			list_of_math = msg.split(",")
			if len(list_of_math) == 4:
				try:
					math_operation = list_of_math[1]
					if "add" in str(math_operation):
						await msgc(float(list_of_math[2]) + float(list_of_math[3]))
					if "sub" in str(math_operation):
						await msgc(float(list_of_math[2]) - float(list_of_math[3]))
					if "mult" in str(math_operation):
						await msgc(float(list_of_math[2]) * float(list_of_math[3]))
					if "div" in str(math_operation):
						await msgc(float(list_of_math[2]) / float(list_of_math[3]))
					if "expo" in str(math_operation):
						await msgc(float(list_of_math[2]) ** float(list_of_math[3]))
					if "root" in str(math_operation):
						await msgc(float(list_of_math[3]) ** (1/float(list_of_math[2])))
					if "sum" in str(math_operation):
						if len(list_of_math[2]) and len(list_of_math[3]) <= 6:
							await msgc(sum(range(int(list_of_math[2]),int(list_of_math[3])+1)))
						else:
							await msgc("Sorry, the range you provided is too large!")
					if "remain" in str(math_operation):
						await msgc(float(list_of_math[2]) % float(list_of_math[3]))
					if "aver" in str(math_operation):
						await msgc(((float(list_of_math[2]) + float(list_of_math[3]))/2))          
				except:
					await msgc("Sorry, the mathematical operations you provided were invalid.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}math, {{operation}}, first number, second number`\nFor example: `{prefix}math, add, 5, 100`")
				embed=discord.Embed(title="Available Operations", color=discord.Colour.red())
				embed.description = math_operations_list(prefix)
				await msgc(embed=embed) 

		if msg.startswith(prefix + 'time'):
			channel = message.channel
			start_time = time.time()
			author = message.author
			await channel.send(f"> :alarm_clock: I have started a stopwatch, {author}. Type `{prefix}stop` to see the result.")

			def check(stop_time):
				return stop_time.content == f'{prefix}stop' and stop_time.channel == channel

			try:
				wait_for_response = await client.wait_for('message', timeout=3600.0, check=check)
			except asyncio.TimeoutError:
				await channel.send('> I have ended the stopwatch now. It has been an hour.')
				return
			else:
				end_time = time.time()
				total_time = end_time - start_time
				formatted_time = "{:.2f}".format(total_time)
				await channel.send("> That was " + formatted_time + " seconds.")

		if msg.startswith(prefix + 'vote'):
			voting_command = msg.split(f"{prefix}vote,")
			if len(voting_command) == 2:
				voting_content = str(voting_command[1]).strip()
				if len(voting_content) < 512:
					vote_title_and_description = (voting_content.split(",", 1))

					if len(vote_title_and_description) == 2:
						vote_title = vote_title_and_description[0]

						if message.channel.permissions_for(message.guild.me).manage_messages:
							await message.delete()

						embed=discord.Embed(title=vote_title, color=discord.Colour.green())

						embed.description = vote_title_and_description[1]

						embed.set_thumbnail(url=message.author.avatar_url)
						embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)

						bot_vote_response = await msgc(embed=embed)      

						await bot_vote_response.add_reaction('✅')
						await bot_vote_response.add_reaction('❌')
					else:
						await msgc(f">>> **Use the format with commas:** `{prefix}vote, vote title, your voting proposal`\n\nFor example: `{prefix}vote, Haircut, Should I get a haircut today?`")
				else:
					await msgc("Sorry, the voting proposal you provided is too long!")
			else:
				await msgc(f">>> **Use the format with commas:** `{prefix}vote, vote title, your voting proposal`\n\nFor example: `{prefix}vote, My Haircut, Should I get a new haircut today?`")

		if msg.startswith(prefix + 'poll'):
			poll_command = msg.split(f"{prefix}poll,")
			if len(poll_command) == 2:
				poll_content = str(poll_command[1]).strip()
				if len(poll_content) < 1000:
					poll_title_and_description = (poll_content.split(",", 1))
					if len(poll_title_and_description) == 2:
						poll_title = poll_title_and_description[0]
						poll_content = poll_title_and_description[1]
						poll_choices = poll_content.strip().split(", ")

						poll_reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣','🔟']
						if len(poll_choices) <= 10 and len(poll_title) < 256:

							embed=discord.Embed(title=poll_title, color=discord.Colour.blue())
							for i in range(0, len(poll_choices)):
								if len(poll_choices[i]) < 256:
									embed.add_field(name=poll_reactions[i] + ' ' + poll_choices[i], value='\n\u200b', inline=False)

							embed.set_thumbnail(url=message.author.avatar_url)
							embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)

							bot_vote_response = await msgc(embed=embed)      
							if message.channel.permissions_for(message.guild.me).manage_messages:
								await message.delete()

							for i in range(0, len(poll_choices)):
								await bot_vote_response.add_reaction(poll_reactions[i])
						else:
							await msgc("You have provided more than 10 options, or your poll title is too long.")
					else:
						await msgc(f">>> **Use the format with commas:** `{prefix}poll, poll title, option 1, option 2, [MAXIMUM 10 OPTIONS]`\n\nFor example: `{prefix}poll, What renovations would you like done?, A new door, A new window, A new furnace`")
				else:
					await msgc("Sorry, the poll you provided is too long!")
			else:
				await msgc(f">>> **Use the format with commas:** `{prefix}poll, poll title, option 1, option 2, [MAXIMUM 10 OPTIONS]`\n\nFor example: `{prefix}poll, What renovations would you like done?, A new door, A new window, A new furnace`")

		if msg.startswith(prefix + 'embed'):
			embed_command = msg.split(f"{prefix}embed,")
			if len(embed_command) == 2:
				embed_message = str(embed_command[1]).strip()
				if len(embed_message) < 512:
					embed_title_and_description = (embed_message.split(",", 1))
					if len(embed_title_and_description) == 2:
						embed_title = embed_title_and_description[0]

						if message.channel.permissions_for(message.guild.me).manage_messages:
							await message.delete()

						embed=discord.Embed(title=embed_title, color=discord.Colour.red())

						embed.description = embed_title_and_description[1]

						embed.set_thumbnail(url=message.author.avatar_url)
						embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)

						await msgc(embed=embed)  
					else:
						await msgc(f">>> **Use the format with a comma:** `{prefix}embed, embed title, embed message`\n\nFor example: `{prefix}embed, Sample Title, Hi everyone! It's great to be here!`")
				else:
					await msgc("Sorry, the embed message you provided is too long!")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}embed, embed title, embed message`\n\nFor example: `{prefix}embed, Sample Title, Hi everyone! It's great to be here!`")

		if msg.startswith(prefix + 'translate'):
			channel = message.channel
			translate_command = msg.split(f"{prefix}translate,")
			if len(translate_command) == 2:
				translate_content = str(translate_command[1]).strip()
				if (len(translate_content) < 1900):
					await msgc("What language would you like to translate this to? (e.g. French)")

					def check(translation_destination):
						return (translation_destination.author.id) == message.author.id and translation_destination.channel == channel

					try:
						destination_language_input = await client.wait_for('message', timeout=30.0, check=check)

					except asyncio.TimeoutError:
						await channel.send("Sorry, I've not yet heard back. Please provide a destination language next time.")
						return
					else:
						destination_language_key = str(destination_language_input.content).lower().strip()

						if "chinese" in destination_language_key:
							await msgc("Is that `simplified` or `traditional`?")

							def check(translation_chinese):
								return (translation_chinese.author.id) == message.author.id and translation_chinese.channel == channel

							try:
								chinese_language_input = await client.wait_for('message', timeout=30.0, check=check)

							except asyncio.TimeoutError:
								await channel.send("Sorry, I've not yet heard back. Please provide a destination language next time.")
								return
							else:
								chinese_language_key = str(chinese_language_input.content).lower().strip()
								if "simpl" in chinese_language_key:
									destination_language_value = translatable_languages["chinese1"]
									translator = google_translator()
									translated_message = translator.translate(translate_content, lang_tgt=destination_language_value)
									await msgc(translated_message)
								elif "trad" in chinese_language_key:
									destination_language_value = translatable_languages["chinese2"]
									translator = google_translator()
									translated_message = translator.translate(translate_content, lang_tgt=destination_language_value)
									await msgc(translated_message)
								else:
									await msgc("Sorry, I don't understand which language you'd like to translate to.")

						elif destination_language_key in translatable_languages:
							destination_language_value = translatable_languages[destination_language_key]
							translator = google_translator()
							translated_message = translator.translate(translate_content, lang_tgt=destination_language_value)
							await msgc(translated_message)

						else:
							await msgc("Sorry, I don't support translation for this language at this time.")
				else:
					await msgc("Sorry, I'm not here to translate an entire essay for you :slight_smile: ")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}translate, message`\n\nFor example: `{prefix}translate, 您好，我是好奇的松饼`")

		if msg.startswith(prefix + 'save'):
			embed=discord.Embed(title="**Store Information**", color=discord.Colour.red())

			embed.description = save_information(prefix)

			await msgc(embed=embed)   

		if msg.startswith(prefix + 'store'):
			author = message.author
			store_information = msg.strip().split("/")

			if len(store_information) == 3:
				saved_information_file = open("information_storage.txt", "a+")
				saved_information_file.seek(0)
				stored_password = str(store_information[1]).strip()
				stored_information = str(store_information[2]).strip()

				passwords_data = []
				for line in saved_information_file:
					line_data = line.strip().split("/")
					passwords = line_data[0]
					passwords_data.append(passwords)
				if stored_password in passwords_data:
					await msgc("> Your password is invalid. Please try again and choose another password.")
					saved_information_file.close()
				else:
					saved_information_file.write("\n" + stored_password + "/" + stored_information)
					await msgc(f"> Your information has been stored. Use `{prefix}save` to view options to access or remove this information at a later time.")
					if message.channel.permissions_for(message.guild.me).manage_messages:
						await message.delete()
					saved_information_file.close()
					information_storage_row = [str(author), str(author.id), stored_information, stored_password]
					information_storage_sheet.insert_row(information_storage_row, 5)
				
			else:
				await msgc(f">>> **Use the format with a slash:** `{prefix}store/ your password/ your information`\n\nFor example: `{prefix}store/password/this is an example of the proper format`")

		if msg.startswith(prefix + 'retrieve'):
			await msgc("**Stored Information Associated with that Password:** " + retrieve_info(msg,prefix))
			if message.channel.permissions_for(message.guild.me).manage_messages:
				await message.delete()

		if msg.startswith(prefix + 'remove'):
			remove_information = msg.strip().split("/")
			if len(remove_information) == 2:
				saved_information_file = open("information_storage.txt", "r+")
				read_only_file = saved_information_file.read()
				saved_information_file.seek(0)
				for line in read_only_file.split("\n"):
					line_data = line.strip().split("/")
					if len(line_data) == 2:
						passwords = line_data[0]
						if passwords != remove_information[1].strip():
							saved_information_file.write(line + "\n")
				saved_information_file.truncate()
				await msgc("> Your information has been removed.")
				saved_information_file.close()
				if message.channel.permissions_for(message.guild.me).manage_messages:
					await message.delete()
			else:
				await msgc(f">>> **Use the format with a slash:** `{prefix}remove/ your password`\n\nFor example: `{prefix}remove/password`")

		dev_command_options = """
			
			We appreciate your feedback, {author} :clap:

			Use `{command_prefix}prefix` to change the command prefix
			Use `{command_prefix}ping` to measure Curious Muffin's response time.
			Use `{command_prefix}feedback` to send feedback or bug reports
			Use `{command_prefix}updates` to view the update changelog
			Use `{command_prefix}help` to view all commands
			
			[Discord Server](https://discord.gg/ZvZmTUnWng)
			[Support Website](https://www.curiousmuffin.ml/contact)

		""".format(command_prefix = prefix, author = message.author)

		if msg.startswith(prefix + 'dev'):
			author = message.author

			embed=discord.Embed(title="Settings Commands", color=discord.Colour.green())

			embed.description = dev_command_options

			await msgc(embed=embed)
		
		if msg.startswith(prefix + 'ping'):
			time_then = time.monotonic()
			await msgc("**Pinging...** :ping_pong: ")
			ping = '%.2f' % (1000*(time.monotonic()-time_then))
			embed=discord.Embed(title="**Bot Latency Information**", color=discord.Colour.green())
			embed.description = "\n**Pong!** The ping is `" + str(ping) + "` milliseconds."
			embed.set_image(url = "https://cdn.discordapp.com/emojis/797164209933910096.gif")
			await msgc(embed=embed)
		
		if msg.startswith(prefix + 'updates'):
			await msgc("Join the Curious Muffin Discord Server to discuss and view everything that's new!")
			await msgc("http://dsc.gg/curious-muffin")

		if msg.startswith(prefix + 'prefix'):
			if message.author.guild_permissions.manage_guild or message.author.guild_permissions.manage_roles:
				channel = message.channel
				author = message.author
				embed=discord.Embed(title="**Prefix Settings**", color=discord.Colour.blurple())
				embed.description = prefix_information(prefix, author)
				await msgc(embed=embed)

				def check(change_prefix_settings_message):
					return (change_prefix_settings_message.author.id) == message.author.id and change_prefix_settings_message.channel == channel and len(change_prefix_settings_message.content) > 0

				try:
					prefix_message = await client.wait_for('message', timeout=30.0, check=check)

				except asyncio.TimeoutError:
					await channel.send("> Your prefix has not been changed.")
					return

				else:
					new_prefix = str(prefix_message.content).strip()
					if "," in new_prefix or "/" in new_prefix or len(new_prefix) > 5:
						await msgc("At this time, `,` and `/` are not available as prefixes.\nYour prefix must also have a **maximum** of 5 characters")
					elif new_prefix == "000":
						await msgc("> Alright, nothing's been changed :slight_smile: ")
					else:
						prefix_file = open('command_prefix.txt', 'r+')
						read_only_prefix_file = prefix_file.read()
						prefix_file.seek(0)
						for line in read_only_prefix_file.split("\n"):
							line_data = line.strip().split(",")
							if len(line_data) == 2:
								guild_id = str(line_data[0]).strip()
								if str(prefix_message.guild.id) != guild_id:
									prefix_file.write(line + "\n")
						prefix_file.write(str(prefix_message.guild.id) + "," + new_prefix + "\n")
						prefix_file.truncate()
						await msgc(f"Great choice! I will now respond to the prefix `{new_prefix}` (e.g. `{new_prefix + 'help'}`)")
						prefix_file.close()
						command_prefix_row = [str(prefix_message.guild.name), str(prefix_message.guild.id), new_prefix]
						command_prefix_sheet.insert_row(command_prefix_row, 5)
			else:
				await msgc("You need to have the `manage server` or `manage roles` privilege in order to change this setting.")

		if msg.startswith(prefix + 'feedback'):
			author = message.author
			feedback_content = msg.split(f"{prefix}feedback,")

			if len(feedback_content) == 2:
				user_feedback = str(feedback_content[1]).strip()
				date_format='%B %d, %Y'
				current_date = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('US/Pacific')).strftime(date_format)

				server_feedback_row = [current_date, str(message.guild.name), str(message.guild.id), str(author), str(author.id), user_feedback]
				server_feedback_sheet.insert_row(server_feedback_row, 5)

				await msgc("Thank you for your feedback! We appreciate it.")
			else:
				await msgc(f">>> **Use the format with a comma:** `{prefix}feedback, your feedback`\n\nFor example: `{prefix}feedback, Nice bot! It would be great if you could implement feature X!`")

		help_command_options = """

		Use `{command_prefix}fun` for fun commands
		Use `{command_prefix}info` for information commands
		Use `{command_prefix}random` for random commands
		Use `{command_prefix}game` for game commands
		Use `{command_prefix}utility` for utility commands
		Use `{command_prefix}dev` for settings or feedback

		""".format(command_prefix = prefix)

		# new_update_category_help = """    
		#   Use `{command_prefix}updates` to view what's new!
		# """.format(command_prefix = prefix) 

		if msg.startswith(prefix + 'help'):
			embed=discord.Embed(title = client.user.name + " Help", color=discord.Colour.blue()) 

			embed.add_field(name="Useful Commands", value=help_command_options, inline=False)
			embed.add_field(name="Join the Curious Muffin Community", value=discord_server_invite, inline=False)
			embed.add_field(name="Useful Links", value=help_command_links, inline=False)
			embed.add_field(name="User Survey! :)", value="https://bit.ly/2VbqTaB", inline=False)

			await msgc(embed=embed)

		prefix_length = len(prefix)
		message_content = (msg.find(prefix)) + prefix_length

		for command in all_available_commands:
			if (msg[message_content:]).startswith(command):
				server_commands_usage_log(str(message.guild.name), str(message.guild.id), str(msg))
				break;
    
keep_alive()
client.run(os.getenv('TOKEN'))