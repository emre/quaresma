from discord import Embed
from datetime import datetime


def get_help():
    """Returns the embed objects of the $help command."""
    embed = Embed(
        color=0x2ecc71,
    )
    embed.add_field(
        name="$subscribe",
        value="Subscribe to a player's matches."
              "```$subscribe <player_account>```",
        inline=False,
    )
    embed.add_field(
        name="$unsubscribe",
        value="Unsubscribe from a player's matches."
              "```$unsubscribe <player_account>```",
        inline=False,
    )

    embed.add_field(
        name="$subscriptions",
        value="Get a list of your subscriptions"
              "```$subscriptions```",
        inline=False,
    )

    embed.add_field(
        name="$help",
        value="Shows this message.",
        inline=False,
    )

    return embed


def subscription_list_embed(discord_account, subscriptions):
    """Returns a rich embed includes the subscription list of a particular
    discord account."""
    print()
    subscription_list = ""
    for subscription in subscriptions:
        subscription_list += f"- {subscription['player_account']}\n"

    embed = Embed(
        color=3447003,
    )
    embed.title = f"Subscriptions of {discord_account}"
    embed.add_field(
        name="Players",
        value=subscription_list,
    )
    embed.timestamp = datetime.utcnow()
    return embed