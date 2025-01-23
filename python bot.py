# Discord bot related libraries
import discord  # Core library for interacting with Discord API. Handles basic bot functionality like receiving and sending messages.
import discord.state  # Provides internal tools for managing the bot's state (e.g., online or idle).
from discord.ext import commands  # Extension library for creating command frameworks (e.g., defining commands like "!help").
from discord.ui import View, Button, Select  # Used to create interactive UI components like buttons and selection boxes to enhance user interaction.

# Asynchronous handling libraries
import asyncio  # Provides asynchronous support for non-blocking operations, ideal for tasks that need to wait (e.g., network requests).
import aiohttp  # Used for making asynchronous HTTP requests, ideal for fetching external API data like weather queries.
import aiofiles  # Used for efficient asynchronous file operations, improving performance when reading or writing large files.

# Standard libraries
import os  # Used for operating system functionalities like reading environment variables (e.g., storing bot tokens) or managing file paths.
import sys  # Interacts with the Python interpreter, supports exiting programs or handling command-line arguments.
import json  # Used for handling JSON data, ideal for reading configuration files or API responses.
import logging  # Used for logging runtime information and error messages, assisting with troubleshooting.
import subprocess  # Used for executing system commands or external programs, e.g., checking if dependencies are installed.
import time  # Provides time-related operations like recording startup time.
import random  # Used for generating random numbers or selecting random data, ideal for building lottery systems, etc.
import re  # Provides regular expression tools for handling string pattern matching, e.g., validating user input.
from datetime import datetime, timedelta, timezone  # Provides date and time operations, e.g., calculating countdowns or formatting dates.

# Configuration and environment management libraries
from dotenv import load_dotenv  # Loads environment variables from a .env file to separate sensitive information from the code.
import yaml  # Used for reading and writing YAML configuration files, suitable for storing multi-layered setup data.
from filelock import FileLock  # Used for file locking, preventing multiple processes from modifying the same file at the same time.

# Other utilities
import psutil  # Used for monitoring system performance and resource usage, e.g., tracking CPU and memory consumption.
from urllib.parse import urlencode  # Encodes URL query parameters, useful for handling API requests with parameters.
from decimal import Decimal, ROUND_DOWN  # Provides high-precision decimal arithmetic, ideal for handling money calculations and scenarios requiring high precision.

# Load environment variables
# By reading from a .env file, sensitive information (like the bot token) is separated from the code for security purposes.
load_dotenv()

# Get the bot token and author's Discord ID
TOKEN = os.getenv('DISCORD_TOKEN_TEST_BOT')  # Fetches the bot's token from environment variables to log in to Discord.
AUTHOR_ID = int(os.getenv('AUTHOR_ID', 0))  # Fetches the author's Discord ID to identify the bot admin.
LOG_FILE_PATH = "feedback_log.txt"  # Specifies the path where log files will be saved.

# Ensure environment variables are correctly set
if not TOKEN or not AUTHOR_ID:
    raise ValueError("Missing required environment variables DISCORD_TOKEN_MAIN_BOT or AUTHOR_ID")  # Raises an error if necessary information is missing.

# Configure the basic logger
# Loggers are helpful for tracking the program's execution, e.g., logging errors, debugging information, or important events.
logging.basicConfig(
    level=logging.INFO,  # Sets the log level to INFO to record general information and errors.
    format='%(asctime)s - %(levelname)s - %(message)s',  # Defines the log output format, including time, level, and message content.
    handlers=[
        logging.FileHandler(filename='main-error.log', encoding='utf-8', mode='w'),  # Saves the logs to the specified file.
        logging.StreamHandler()  # Outputs the log information to the console in real-time.
    ]
)

# Set up Discord bot permissions (Intents)
# Intents determine which events the bot can receive, such as member joins or message content.
intents = discord.Intents.default()  # Initializes the default basic permissions.
intents.message_content = True  # Enables the permission to receive message content, allowing the bot to process user messages.
intents.guilds = True  # Enables receiving server-related events, such as joining or leaving a server.
intents.members = True  # Enables receiving member-related events, such as member joins or updates.

# Initialize bot instance
bot = commands.Bot(command_prefix='!', intents=intents)  # Creates the bot object with a command prefix of "!".

# Global variable: Used to record the bot's startup time
start_time = time.time()  # Records the start time of the bot's launch.

# Event handler: Handles incoming message events
@bot.event
async def on_message(message):
    global last_activity_time  # Uses a global variable to record the last activity time.

    # Ignore messages from the bot itself to avoid a response loop.
    if message.author == bot.user:
        return

    # Ensure other command handlers process the message correctly, preventing event conflicts.
    await bot.process_commands(message)

# Bot startup event: Sets bot's status and shows startup information
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")  # Displays the bot's name and ID for login verification.
    print("------")

    print("Slash commands have been automatically synchronized.")  # Indicates successful synchronization of the bot's slash commands.

    try:
        # Set the bot's presence and activity
        await bot.change_presence(
            status=discord.Status.idle,  # Sets the bot's status to idle.
            # Other possible statuses:
            # - discord.Status.online: Sets the bot as "online".
            # - discord.Status.dnd: Sets the bot as "Do Not Disturb".
            # - discord.Status.invisible: Sets the bot as "invisible", not visible to others.
            activity=discord.Activity(
                type=discord.ActivityType.playing,  # Sets the activity type to "playing".
                # Other possible activity types:
                # - discord.ActivityType.listening: Sets to "listening", e.g., listening to music.
                # - discord.ActivityType.watching: Sets to "watching", e.g., watching a video or stream.
                # - discord.ActivityType.streaming: Sets to "streaming", suitable for live streaming.
                name='Blue Archive'  # Sets the activity name, e.g., the current game or activity the bot is engaged in.
            )
        )
        print("Bot status has been set.")
    except Exception as e:
        print(f"Failed to set presence: {e}")  # Logs an error if setting the presence fails.

    # Record the time taken for the bot to start up
    end_time = time.time()
    startup_time = end_time - start_time  # Calculates the time from startup to readiness.
    print(f'Bot startup time: {startup_time:.2f} seconds')  # Displays the bot's startup time.

    # List the servers the bot is currently in
    print('List of servers the bot is in:')
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')  # Prints the server name and ID.

    # Record the bot's last activity time
    global last_activity_time
    last_activity_time = time.time()

# Main function: Starts the bot
try:
    bot.run(TOKEN, reconnect=True)  # Starts the bot with automatic reconnection enabled.
except discord.LoginFailure:
    print("Invalid bot token. Please check the TOKEN.")  # Informs the user if the token is invalid (e.g., not set or in wrong format).
except Exception as e:
    print(f"An error occurred while starting the bot: {e}")  # Catches other startup errors, e.g., network issues.
