from discord.ext import commands
import requests
import json

url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

class Summary(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["summary", "summarise"])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def summariser(self, ctx, *, prompt):
        async with ctx.typing():
            payload = json.dumps({
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "min_length": 50
                }
            })

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer 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'
            }

            response = requests.post(url, headers=headers, data=payload)

            try:
                await ctx.send(response.json()[0]["summary_text"])
            except Exception as e:
                await ctx.send(e)

async def setup(client):
    await client.add_cog(Summary(client))
