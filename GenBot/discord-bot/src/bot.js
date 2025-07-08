const { Client, Intents } = require('discord.js');
require('dotenv').config();
const pingCommand = require('./commands/ping');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', message => {
    if (message.content === '!ping') {
        pingCommand.execute(message);
    }
});

client.login(process.env.TOKEN);