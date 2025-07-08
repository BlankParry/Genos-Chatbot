# Discord Bot Setup Guide

This README provides instructions on how to create and set up your Discord bot.

## Table of Contents
1. [Create a Discord Application](#create-a-discord-application)
2. [Get Your Bot Token](#get-your-bot-token)
3. [Set Up Your Project](#set-up-your-project)
4. [Create the `.env` File](#create-the-env-file)
5. [Implement the Bot Logic](#implement-the-bot-logic)
6. [Run Your Bot](#run-your-bot)
7. [Invite Your Bot to a Server](#invite-your-bot-to-a-server)

## Create a Discord Application
- Go to the Discord Developer Portal.
- Click on "New Application" and give it a name.
- Navigate to the "Bot" tab and click "Add Bot".

## Get Your Bot Token
- Under the Bot tab, click "Copy" to copy your bot token. You will need to paste this into your `.env` file.

## Set Up Your Project
- Create a new directory for your project and navigate into it.
- Run `npm init -y` to create a `package.json` file.
- Install the Discord.js library by running `npm install discord.js`.

## Create the `.env` File
- In the root of your project, create a `.env` file.
- Add the following lines, replacing `YOUR_BOT_TOKEN` with your actual bot token:
  ```
  TOKEN=YOUR_BOT_TOKEN
  ```

## Implement the Bot Logic
- In `src/bot.js`, set up the bot to log in and respond to messages.
- In `src/commands/ping.js`, implement the logic for the "ping" command.

## Run Your Bot
- Add a start script in your `package.json`:
  ```
  "scripts": {
    "start": "node src/bot.js"
  }
  ```
- Run your bot using `npm start`.

## Invite Your Bot to a Server
- Go back to the Discord Developer Portal, navigate to the "OAuth2" tab, and select the "bot" scope.
- Choose the permissions your bot needs and copy the generated URL.
- Open the URL in your browser and invite your bot to your server.

Now your Discord bot should be set up and ready for deployment!