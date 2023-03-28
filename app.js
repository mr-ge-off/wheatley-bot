import * as dotenv from 'dotenv';
import { Client, GatewayIntentBits } from 'discord.js';

// configure env vars and secrets ;)
dotenv.config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}.`);
});

client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName === 'gik') {
        await interaction.reply('gak!');
    }
    else if (interaction.commandName === 'gak') {
        await interaction.reply('gik!');
    }
});

client.login(process.env.DISCORD_TOKEN);

