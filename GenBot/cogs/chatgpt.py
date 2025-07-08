from discord.ext import commands
import requests
import os

url = "https://chatgpt-42.p.rapidapi.com/gpt4"

class ChatGPT(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["chatgpt", "gpt", "answer", "ChatGPT", "Chatgpt", "chat"])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def slavegpt(self, ctx, *, prompt):
        async with ctx.typing():
            payload = {
                "messages": [{
                    "role": "user",
                    "content": prompt
                }],
                "web_access": False,
            }

            headers = {
	        "x-rapidapi-key": os.getenv("rapid_api_key"),
	        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
	        "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

            try:
                await ctx.send(response.json()['result'])
            except Exception:
                print(response.json())
                await ctx.send("Unexpected Error Occurred")

async def setup(client):
    await client.add_cog(ChatGPT(client))
