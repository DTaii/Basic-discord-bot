import discord
from discord.ext import commands

# Declare the Discord bot token
TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True

# Create the bot and set command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Command !hello
@bot.command()
async def hello(ctx):
    # Create an Embed object to send a more stylish message
    embed = discord.Embed(
        title='Hello!',
        description=f'Hello {ctx.author.mention}, have a great day! 🔥🔥',
        color=discord.Color.green()  # Color of the Embed
    )
    # Add a GIF image to the Embed
    embed.set_image(url='https://example.com/your-gif-url-here.gif')
    # Send the message with the Embed
    await ctx.send(embed=embed)

# Command !reply (message)
@bot.command()
async def reply(ctx, *, message):
    # Check if the user has permission to delete messages
    if ctx.author.guild_permissions.manage_messages:
        try:
            # Reply with the provided message
            await ctx.send(message)
            # Delete the user's command message
            await ctx.message.delete()
        except discord.Forbidden:
            await ctx.send("Bot doesn't have enough permissions to delete messages.")
    else:
        await ctx.send("You don't have permission to delete messages!")

# Command !ping
@bot.command()
async def ping(ctx):
    # Command to check if the bot is active
    await ctx.send('Pong!')

# Command !slap
@bot.command()
async def slap(ctx, member: discord.Member):
    # Create an Embed object to send a more stylish message
    embed = discord.Embed(
        title='',
        description=f'{ctx.author.mention} slapped {member.mention}!🔥🔥',
        color=discord.Color.red()  # Color of the Embed
    )
    # Add a GIF image to the Embed
    embed.set_image(url='https://example.com/your-gif-url-here.gif')
    # Send the message with the Embed
    await ctx.send(embed=embed)

# Command !hug
@bot.command()
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(
        title='',
        description=f'{ctx.author.mention} hugged {member.mention}!🫂',
        color=discord.Color.red()
    )
    embed.set_image(url='https://example.com/your-gif-url-here.gif')
    await ctx.send(embed=embed)


# Command !createcategory to create a category and channel
@bot.command()
async def createcategory(ctx, category_name, channel_name, channel_type):
    # Check if the channel type is valid
    valid_channel_types = ['text', 'voice']
    if channel_type not in valid_channel_types:
        await ctx.send('Invalid channel type. Use "text" or "voice".')
        return

    # Create the category
    category = await ctx.guild.create_category(category_name)

    # Create a channel based on the type
    if channel_type == 'text':
        await ctx.guild.create_text_channel(channel_name, category=category)
    elif channel_type == 'voice':
        await ctx.guild.create_voice_channel(channel_name, category=category)

    # Send a message to the command sender
    await ctx.send(f'Created category "{category_name}" and channel "{channel_name}" of type "{channel_type}" successfully.')

# Command !createchannel to create a channel within an existing category
@bot.command()
async def createchannel(ctx, category_name, channel_name, channel_type):
    # Check if the channel type is valid
    valid_channel_types = ['text', 'voice']
    if channel_type not in valid_channel_types:
        await ctx.send('Invalid channel type. Use "text" or "voice".')
        return

    # Find the category by name
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    if not category:
        await ctx.send(f'Category "{category_name}" does not exist.')
        return

    # Create a channel based on the type
    if channel_type == 'text':
        await category.create_text_channel(channel_name)
    elif channel_type == 'voice':
        await category.create_voice_channel(channel_name)

    # Send a message to the command sender
    await ctx.send(f'Created channel "{channel_name}" of type "{channel_type}" in category "{category_name}" successfully.')

# Command !deletecategory to delete a category and all its channels
@bot.command()
async def deletecategory(ctx, category_name):
    # Find the category by name
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    if not category:
        await ctx.send(f'Category "{category_name}" does not exist.')
        return

    # Loop through and delete all channels in the category
    for channel in category.channels:
        await channel.delete()

    # Delete the category
    await category.delete()
    await ctx.send(f'Deleted category "{category_name}" and all its channels successfully.')

# Command !deletechannel to delete a channel within a category
@bot.command()
async def deletechannel(ctx, category_name, channel_name):
    # Find the category by name
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    if not category:
        await ctx.send(f'Category "{category_name}" does not exist.')
        return

    # Find the channel within the category
    channel = discord.utils.get(category.channels, name=channel_name)

    if not channel:
        await ctx.send(f'Channel "{channel_name}" does not exist in category "{category_name}".')
        return

    # Delete the channel
    await channel.delete()
    await ctx.send(f'Deleted channel "{channel_name}" in category "{category_name}" successfully.')

# Command !setup to automatically set up basic categories and channels
@bot.command()
async def setup(ctx):
    # Create a category "Announcements"
    category_announcements = await ctx.guild.create_category("Announcements")

    # Create a text channel "Rules"
    await ctx.guild.create_text_channel("Rules", category=category_announcements)
    await ctx.guild.create_text_channel("Welcome", category=category_announcements)
    await ctx.guild.create_text_channel("Goodbye", category=category_announcements)

    # Create a category "Entertainment"
    category_entertainment = await ctx.guild.create_category("Entertainment")

    # Create a text channel "Chat"
    await ctx.guild.create_text_channel("Chat", category=category_entertainment)
    await ctx.guild.create_text_channel("Spambot", category=category_entertainment)
    await ctx.guild.create_text_channel("Game Chat", category=category_entertainment)
