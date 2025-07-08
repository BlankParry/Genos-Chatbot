from discord.ext import commands
import discord
import os
import requests
import aiohttp
from io import BytesIO

url = "https://chatgpt-42.p.rapidapi.com/texttoimage3"

class DallE(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["DallE", "Dalle", "dalle", "imagine", "image"])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def dall_e(self, ctx, *, prompt):
        async with ctx.typing():
            payload = {
                "text": prompt,
                "width": 1024,
                "height": 1024
            }  # Fixed: Added missing closing brace

            headers = {
                "x-rapidapi-key": os.getenv("rapid_api_key"),
                "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
                "Content-Type": "application/json"
            }  # Fixed: Added missing closing brace

            response = requests.post(url, json=payload, headers=headers)
            
            try:
                data = response.json()
                image_url = data['generated_image']
                
                # Download the image and send as file attachment
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            
                            # Send as direct file attachment (no embed)
                            image_file = discord.File(
                                BytesIO(image_data), 
                                filename="generated_image.png"
                            )
                            
                            await ctx.send(f"**Generated image for:** {prompt}", file=image_file)
                        else:
                            await ctx.send("❌ Failed to download image")
                            
            except Exception as e:
                print(f"Error: {e}")
                await ctx.send(f"❌ Error: {e}")

async def setup(client):
    await client.add_cog(DallE(client))
