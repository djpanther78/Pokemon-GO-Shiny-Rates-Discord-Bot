# Pokemon-GO-Shiny-Rates-Discord-Bot
A Discord bot to display the Shiny rates of your Golbat instance from the last 24 hours. Using NextCord, Python and MySQL-Connector

# Instructions:
1. Edit the .env file. Here is an example:

DISCORD_TOKEN=DiscordBotTokenHere <br />
DB_HOST=DBHostHere (`ServerIP or Localhost` in most cases) <br />
DB_PORT=DBPortHere (`3306` in most cases) <br />
DB_NAME=DBNameHere (`golbat` in most cases) <br />
DB_USER=DBUserNameHere <br />
DB_PASSWORD=DBPasswordhere <br />
GUILD_ID=DiscordServerIDHere <br />

2. `python -m pip install -r requirements.txt`
3. Start the bot. PM2 recommended (`npm install -g pm2`) `pm2 start bot.py --name shinyratesdiscordbot`
