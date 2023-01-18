# DiscordBot

Personal discord bot that has multiple jobs.

## What does it do ?

The bot is still in construction but right now it can respond very simple sentences to specific commands and some games are on their way !

### Game 1 - FlagGuesser

Thanks to <https://flagpedia.net>, the bot has a database of all country flags (and even flags of sub-country as the U.S. states).

## Setup

If you want to use create your own version of this bot, clone the repository and change the file `.env.example` to `.env`.

Do not forget to enter the right token of your bot.
If you do not know how to create a bot, or where to find its token, here is the official documentation on the matter: <https://discordpy.readthedocs.io/en/stable/discord.html>.

For the `GENERAL_ID` environment variable in the `.env`, it should be the ID of the channel you want your bot to say "I'm online" and "I'm disconnecting". If you do not want the bot to say that, set it to `None`. It is worth noting that setting this ID has no impact on where the bot can respond or read the message.
