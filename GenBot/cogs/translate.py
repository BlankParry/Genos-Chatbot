from discord.ext import commands
import requests
import os

url = "https://text-translator2.p.rapidapi.com/translate"

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def translate(self, ctx, source, target, *, prompt):
        async with ctx.typing():
            payload = {
                "source_language": source,
                "target_language": target,
                "text": prompt
            }
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": os.getenv('rapid_api_key'),
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
            }

            response = requests.post(url, data=payload, headers=headers)

            try:
                await ctx.send(response.json()['data']['translatedText'])
            except Exception:
                print(response.json())
                await ctx.send("Unexpected Error Occurred")

async def setup(client):
    await client.add_cog(Translate(client))
