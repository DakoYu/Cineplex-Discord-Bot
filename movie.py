import requests, discord, dotenv, os
from discord.ext import commands

# Initalize the token
dotenv.load_dotenv()

token = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')

def movie_info(movie):
    movie_data = {
                    'name': movie['name'],
                    'url': movie['urlSlug'],
    }

    return movie_data


def movies_handler(language, is_on=True):
    url = 'https://www.cineplex.com/api/v1/movies/'

    res = requests.get(url)

    data = res.json()

    movies = []

    for movie in data['data']:
        if movie['marketLanguageCode'] == language:
            if movie['isNowPlaying'] == is_on:
                movie_data = movie_info(movie)
                movies.append(movie_data)

    movies.sort(key=lambda key: key['name'])

    return movies


def embed_generator(title, description):
    embed = discord.Embed(
        title=title,
        url='https://www.cineplex.com/',
        description=description,
        color=0x206694
    )

    embed.set_author(
        name='Cineplex',
        url='https://www.cineplex.com',
    )

    return embed

def embed_add_movies(embed, movies):
    for movie in movies:
        name = movie['name']
        url = f'https://www.cineplex.com/movie/{movie["url"]}'

        embed.add_field(
            name=name,
            value=url,
            inline=False
        )

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')

@bot.command(name='movies')
async def test(ctx, arg1='EN'):
    embed = embed_generator(
        '🍿🍿🍿WHAT\'S ON🍿🍿🍿',
        'EXPERIENCE THE NEWEST MOVIE IN CINEPLEX'
        )

    movies = movies_handler(arg1)

    embed_add_movies(embed, movies)

    await ctx.send(embed=embed)

@bot.command(name='future')
async def get_movies(ctx, arg1='EN'):
    embed = embed_generator(
        '📅📅📅FUTURE MOVIES📅📅📅',
        'FUTURE MOVIE RELEASE IN CINEPLEX'
        )

    movies = movies_handler(arg1, False)

    embed_add_movies(embed, movies)

    await ctx.send(embed=embed)

@bot.command(name='commands')
async def commands(ctx):
    embed = discord.Embed(
        title='🎥Cineplex Bot Commands',
        description='A list of commands for the bot',
        color=0x2ecc71
    )

    embed.add_field(
        name='**!movies**',
        value='The command will display the newest movies in the theater\nYou can also use **!movies FR** to get movies in french!',
        inline=False
    )

    embed.add_field(
        name='**!future**',
        value='The command will display the future release movies in the theater\nYou can also use **!future FR** to get future release movies in french!',
        inline=False
    )


    await ctx.send(embed=embed)

bot.run(token)