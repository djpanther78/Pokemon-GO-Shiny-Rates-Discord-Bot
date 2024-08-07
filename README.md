# Pokemon-GO-Shiny-Rates-Discord-Bot
A Discord bot to display the Shiny rates of your Golbat instance from the last 24 hours. Using NextCord, Python and MySQL-Connector

# Instructions:
1. Edit the .env file. Here is an example:

`DISCORD_TOKEN=DiscordBotTokenHere
DB_HOST=DBHostHere (`ServerIP or Localhost` in most cases)
DB_PORT=DBPortHere (`3306` in most cases)
DB_NAME=DBNameHere (`golbat` in most cases)
DB_USER=DBUserNameHere
DB_PASSWORD=DBPasswordhere
GUILD_ID=DiscordServerIDHere`

2. `python -m pip install -r requirements.txt`
3. Start the bot. PM2 recommended (`npm install -g pm2`) `pm2 start bot.py --name shinyratesdiscordbot`
