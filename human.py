import asyncio

async def simulate(message):
     # Wait a bit to simulate the reading of the message
    await asyncio.sleep(1)
    # Display a typing indicator while the bot is thinking
    async with message.channel.typing():
        await asyncio.sleep(1)