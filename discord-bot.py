import discord
import os

# Replace with your actual token




intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    
    # Get channel
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel not found!")
        return

    # Send initial status
    await channel.send("🟢 Bot is online and ready to log trades.")
    
    # Send a demo trade message
    await channel.send("📈 Demo Trade: Bought 0.01 BTC @ $68,000")

# Optional function for future logging use
async def log_trade(message):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("❌ Channel not found!")

client.run(DISCORD_BOT_TOKEN)
