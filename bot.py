import nextcord
from nextcord.ext import commands
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from decimal import Decimal

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.slash_command(name='shinyrates', description='Get shiny rates for a Pokémon')
async def shiny_rates(interaction: nextcord.Interaction, pokemon_name: str):
    if interaction.guild.id != GUILD_ID:
        await interaction.response.send_message("This command can only be used in the specific guild.")
        return

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
    
    if response.status_code != 200:
        await interaction.response.send_message('Pokémon not found.')
        return

    data = response.json()
    pokemon_id = data['id']
    pokemon_name = data['name'].capitalize()
    sprite_url = f"https://github.com/nileplumb/PkmnShuffleMap/blob/master/UICONS/pokemon/{pokemon_id}.png?raw=true"

    connection = get_db_connection()
    if connection is None:
        await interaction.response.send_message("Cannot connect to the database.")
        return

    cursor = connection.cursor(dictionary=True)

    twenty_four_hours_ago = datetime.now() - timedelta(days=1)
    formatted_time = twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')

    query = """
    SELECT i.pokemon_id,
           SUM(i.`count`) AS pokemoncount,
           (SELECT SUM(s.`count`) FROM pokemon_shiny_stats s WHERE i.pokemon_id = s.pokemon_id AND i.date = s.date) AS shiny,
           (SELECT SUM(h.`count`) FROM pokemon_hundo_stats h WHERE i.pokemon_id = h.pokemon_id AND i.date = h.date) AS hundo,
           (SELECT SUM(n.`count`) FROM pokemon_nundo_stats n WHERE i.pokemon_id = n.pokemon_id AND i.date = n.date) AS nundo
    FROM pokemon_stats i
    WHERE i.date >= %s AND i.pokemon_id = %s
    GROUP BY i.pokemon_id
    ORDER BY pokemoncount DESC
    """

    try:
        cursor.execute(query, (formatted_time, pokemon_id))
        result = cursor.fetchall()

        if not result:
            await interaction.response.send_message('No data found for this Pokémon in the last 24 hours.')
            cursor.close()
            connection.close()
            return

        pokemon_data = result[0]

        shiny_count = Decimal(pokemon_data.get('shiny', 0) or 0)
        hundo_count = Decimal(pokemon_data.get('hundo', 0) or 0)
        nundo_count = Decimal(pokemon_data.get('nundo', 0) or 0)
        pokemon_count = Decimal(pokemon_data.get('pokemoncount', 0) or 0)

        shiny_rate = f"1/{round(pokemon_count / shiny_count)}" if shiny_count > 0 else 'N/A'
        hundo_rate = f"1/{round(pokemon_count / hundo_count)}" if hundo_count > 0 else 'N/A'
        nundo_rate = f"1/{round(pokemon_count / nundo_count)}" if nundo_count > 0 else 'N/A'

        embed = nextcord.Embed(title=f'Shiny Rates for {pokemon_name}', color=0x00ff00)
        embed.set_thumbnail(url=sprite_url)
        embed.add_field(name='Total Count', value=str(pokemon_count), inline=False)
        embed.add_field(name='Shiny Count', value=str(shiny_count), inline=False)
        embed.add_field(name='Shiny Rate', value=shiny_rate, inline=False)
        embed.add_field(name='Hundo Count', value=str(hundo_count), inline=False)
        embed.add_field(name='Hundo Rate', value=hundo_rate, inline=False)
        embed.add_field(name='Nundo Count', value=str(nundo_count), inline=False)
        embed.add_field(name='Nundo Rate', value=nundo_rate, inline=False)

        await interaction.response.send_message(embed=embed)
    except Error as e:
        print(f"Error executing query: {e}")
        await interaction.response.send_message("An error occurred while fetching data.")
    finally:
        cursor.close()
        connection.close()

bot.run(TOKEN)
