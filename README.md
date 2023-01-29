# DiscordBot

Personal discord bot that has multiple jobs.

## What does it do ?

The bot is still in construction but right now it can respond very simple sentences to specific commands and some games are on the way !

### All commands

These are all the commands, in the format `$command_name <required> [optional]`. *`[*args]` means there might be several optional arguments.*

- `$hack [target]`: It may or may not hack the person you target :eyes:.
- `$thread?`: Says if you are is a **Thread** or a **Text Channel**.
- `good bot`: This is the only command without the "$" prefix. It is a reddit reference.

- `$game <game_name> [*args]`: Creates a game. Takes arguments: *see [Games](#games)*.
- `$play [*args]`: Command used in games. Takes arguments: *see [Games](#games)*.
- `$end`: Command used in games. *see [Games](#games)*.
- `$delete`: Deletes the thread. Must be applied in a **Thread** associated to a game.
- `$ongoing_games`: Lists all the ongoing games (only in Channels and not in DMs) the Bot is holding.

- `$delete_all`: **Administrator only**. Deletes all the threads of a TextChannel that has been created by the bot.
- `$offline`: **Administrator only**. Disconnects the bot from discord.

### Games

Games are created by the command `$game`. See the following sections to know what arguments are requested for each game.
The command `$game` to create a game is only authorized in **Text Channel** (or in **DM**, see [Play in DMs](#play-in-dms)) and the command (if everything goes right) will create a **Thread** where the game will be played.

In the thread of a game, the players can type `$play` or `$end`, see in the following sections what they do.

To see how many and where there are ongoing games, type `$ongoing_games`, it will give you the links to the threads where there are an unfinished game!

#### FlagGuesser

Thanks to <https://flagpedia.net>, the bot has a database of all country flags (and even flags of sub-country as the U.S. states).

##### Create the game

To create the game, type:

```sh
$game flag difficulty language
```

where `difficulty` and `language` are optional.
`difficulty` can be:

- `easy` (default): only countries
- `hard`: all countries and subcountries (as US States and overseas departments/regions)
- `us`: only flags of the US States and US territories
- `eu`: only european countries

`language` will be the language requested for the answers and can be:

- `fr` (default): French
- `en`: English

This will create a thread where the game will take place.

##### How to play

In the thread of the game, as long as it is not finished, you can type:

```sh
$play country
```

where `country` is the country you think the flag belongs to.
The bot will say if it is correct or not.
The game ends only if you found the right answer or if you type:

```sh
$end
```

This command will end the game and the bot will give the answer.

##### Specifities about the check between your answer and the answers

For some countries, there are several correct names, so it means there can be several correct answers. For instance, *Czech Republic* is as correct as *Czechia*.

For the validation, the bot transforms both the player's answer and the expected answers:

- the string is converted to lowercase,
- accented characters are changed to their plain ascii equivalent,
- hyphens become spaces,
- and then non-letters (numbers, ponctuation, ...) are removed. *this is one is actually an arbitrary choice and could be discussed*.

For instance: *São Tomé and Príncipe* becomes *sao tome and principe*. *Nouvelle-Zélande* becomes *nouvelle zelande*. *Fr3ance!" becomes "france*.
This means that if you answered *Sao Tomé and Principe* (and it was the country to find), your answer will be considered as correct, even if this writing is not technically the same as *São Tomé and Príncipe*.

### Play in DMs

Games can be played in DMs with the bot. It will be the same as if it is a *TextChannel* but there will be no *Threads* created, it will be directly in the DM with the bot, as Threads cannot be created there.

There can be only one game at a time in the DM with the bot.

To play in DM, right-click the bot and choose to send it a message. The commands then stay the same.

## Setup

If you want to use create your own version of this bot, clone the repository and change the file `.env.example` to `.env`.

Do not forget to enter the right token of your bot.
If you do not know how to create a bot, or where to find its token, here is the official documentation on the matter: <https://discordpy.readthedocs.io/en/stable/discord.html>.

For the `GENERAL_ID` environment variable in the `.env`, it should be the ID of the channel you want your bot to say "I'm online" and "I'm disconnecting". If you do not want the bot to say that, set it to `None`. It is worth noting that setting this ID has no impact on where the bot can respond or read the message.

## Permissions needed for the bot

Overall the bot must be allowed to:

- send messages
- read messages / see history
- react to messages
- create and delete threads
- send link
- use emoji / external emoji
- mention users
- send images / files

## Running tests

Some tests are in the folder `test`.
To run them, go at the root of the project and type

```sh
pytest
```

## Nota bene

`$hack` does not hack.
