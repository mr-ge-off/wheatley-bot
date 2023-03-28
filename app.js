import * as dotenv from 'dotenv';
import { Client, Collection, Events, GatewayIntentBits } from 'discord.js';

import text from './commands/text.js';


// configure env vars and secrets ;)
dotenv.config();

const addCommandsToCollection = (commands, collection) => {
    for (const command of commands) {
        collection.set(command.attribs.name, command)
    }
}

const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.commands = new Collection();

// add in all command sub-categories
addCommandsToCollection(text, client.commands);

client.on(Events.ClientReady, () => {
    console.log(`Logged in as ${client.user.tag}.`);
});

client.on(Events.InteractionCreate, async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) {
        interaction.reply({ content: "Hey dipshit, that's not a real command.", ephemeral: true });
        return;
    }
    
    try {
        await command.execute(interaction);
    }
    catch (error) {
        console.error(error);
    }

});

client.login(process.env.DISCORD_TOKEN);

