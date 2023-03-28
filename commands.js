import { REST, Routes } from 'discord.js';
import * as dotenv from 'dotenv';


// configure env vars and client secrets :D
dotenv.config();

const GG_COMMANDS = [
    {
        name: 'gak',
        description: 'gik!',
        type: 1,
    },
    {
        name: 'gik',
        description: 'gak!',
        type: 1,
    }
];

const allCommands = [
    ...GG_COMMANDS
];

const registerCommands = async (whichCommands, isGlobal=true) => {
    const restClient = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);
    let routeParams = [process.env.APPLICATION_ID];
    if (!isGlobal) {
        routeParams.push(process.env.GUILD_ID);
    }

    try {
        console.log('starting command refresh...');
        await restClient.put(
            Routes.applicationCommands(...routeParams),
            { body: allCommands }
        );
        console.log('refreshed commands!');
    }
    catch (error) {
        console.error(error);
    }
};


registerCommands(allCommands);
