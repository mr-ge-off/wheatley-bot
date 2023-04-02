import * as dotenv from 'dotenv';
import { Client, Collection, Events, GatewayIntentBits } from 'discord.js';

import text from './commands/text';
import voice from './commands/voice';
import silly from './commands/silly';
import admin, { lockUserInstance } from './commands/admin';
import { CommandTuple, CommandClient, CommandCollection } from './myTypes';


// configure env vars and secrets ;)
dotenv.config();

const addCommandsToCollection = (commands: CommandTuple[], collection: CommandCollection) => {
    for (const command of commands) {
        collection.set(command.attribs.name, command)
    }
}

const client = (new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates] })) as CommandClient;
client.commands = new Collection<string, CommandTuple>();

// add in all command sub-categories
addCommandsToCollection(text, client.commands);
addCommandsToCollection(voice, client.commands);
addCommandsToCollection(silly, client.commands);
addCommandsToCollection(admin, client.commands);

client.once(Events.ClientReady, () => {
    console.log(`Logged in as ${client.user?.tag}.`);
});

client.on(Events.InteractionCreate, async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    const command = (interaction.client as CommandClient).commands.get(interaction.commandName);

    if (!command) {
        interaction.reply({ content: "Hey dipshit, that's not a real command.", ephemeral: true });
        return;
    }
    
    try {
        if (lockUserInstance) {
            
            // unlock cmd always allowed by admins
            if (lockUserInstance !== interaction.user && command !== admin[1]) {
                interaction.reply({
                    content: `I'm locked right now to ${lockUserInstance}`,
                    ephemeral: true,
                    target: interaction.user  });

                return;
            }
        }
        await command.execute(interaction);
    }
    catch (error) {
        console.error(error);
    }
});

client.login(process.env.DISCORD_TOKEN);

