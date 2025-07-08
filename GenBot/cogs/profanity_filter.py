from discord.ext import commands
import discord
import json
import os
from datetime import datetime, timedelta

class ProfanityFilter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.profanity_file = "profanity_words.json"
        self.warnings_file = "user_warnings.json"
        self.load_data()
        
    def load_data(self):
        # Load profanity words
        if os.path.exists(self.profanity_file):
            with open(self.profanity_file, 'r') as f:
                self.banned_words = json.load(f)
        else:
            self.banned_words = ["badword1", "badword2", "example"]  # Default words
            self.save_profanity_words()
            
        # Load user warnings
        if os.path.exists(self.warnings_file):
            with open(self.warnings_file, 'r') as f:
                self.user_warnings = json.load(f)
        else:
            self.user_warnings = {}
    
    def save_profanity_words(self):
        with open(self.profanity_file, 'w') as f:
            json.dump(self.banned_words, f, indent=2)
    
    def save_warnings(self):
        with open(self.warnings_file, 'w') as f:
            json.dump(self.user_warnings, f, indent=2)
    
    def contains_profanity(self, message):
        message_lower = message.lower()
        for word in self.banned_words:
            if word.lower() in message_lower:
                return True
        return False
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        if self.contains_profanity(message.content):
            await message.delete()
            
            user_id = str(message.author.id)
            if user_id not in self.user_warnings:
                self.user_warnings[user_id] = 0
                
            self.user_warnings[user_id] += 1
            warnings = self.user_warnings[user_id]
            
            if warnings < 3:
                await message.channel.send(
                    f"⚠️ {message.author.mention}, please watch your language! "
                    f"Warning {warnings}/3"
                )
            else:
                # Timeout for 10 minutes
                timeout_until = discord.utils.utcnow() + timedelta(minutes=1)
                try:
                    await message.author.timeout(timeout_until, reason="Exceeded profanity warnings")
                    await message.channel.send(
                        f"🔇 {message.author.mention} has been timed out for 10 minutes due to repeated profanity."
                    )
                    self.user_warnings[user_id] = 0  # Reset warnings
                except discord.Forbidden:
                    await message.channel.send("❌ I don't have permission to timeout this user.")
                except Exception as e:
                    await message.channel.send(f"❌ Error timing out user: {e}")
            
            self.save_warnings()
    
    # Admin commands to manage the word list
    @commands.command(name="addword")
    @commands.has_permissions(administrator=True)
    async def add_word(self, ctx, *, word):
        """Add a word to the profanity filter"""
        if word.lower() not in [w.lower() for w in self.banned_words]:
            self.banned_words.append(word.lower())
            self.save_profanity_words()
            await ctx.send(f"✅ Added '{word}' to the profanity filter.")
        else:
            await ctx.send(f"❌ '{word}' is already in the filter.")
    
    @commands.command(name="removeword")
    @commands.has_permissions(administrator=True)
    async def remove_word(self, ctx, *, word):
        """Remove a word from the profanity filter"""
        word_lower = word.lower()
        original_words = [w for w in self.banned_words if w.lower() == word_lower]
        
        if original_words:
            for w in original_words:
                self.banned_words.remove(w)
            self.save_profanity_words()
            await ctx.send(f"✅ Removed '{word}' from the profanity filter.")
        else:
            await ctx.send(f"❌ '{word}' is not in the filter.")
    
    @commands.command(name="listwords")
    @commands.has_permissions(administrator=True)
    async def list_words(self, ctx):
        """List all words in the profanity filter"""
        if self.banned_words:
            word_list = ", ".join(self.banned_words)
            await ctx.send(f"🚫 **Banned words:** {word_list}")
        else:
            await ctx.send("📝 No words in the profanity filter.")
    
    @commands.command(name="clearwarnings")
    @commands.has_permissions(administrator=True)
    async def clear_warnings(self, ctx, member: discord.Member = None):
        """Clear warnings for a specific user or all users"""
        if member:
            user_id = str(member.id)
            if user_id in self.user_warnings:
                del self.user_warnings[user_id]
                self.save_warnings()
                await ctx.send(f"✅ Cleared warnings for {member.mention}")
            else:
                await ctx.send(f"❌ {member.mention} has no warnings.")
        else:
            self.user_warnings = {}
            self.save_warnings()
            await ctx.send("✅ Cleared all user warnings.")

async def setup(client):
    await client.add_cog(ProfanityFilter(client))
