import { REST, Routes } from 'discord.js';
import * as dotenv from 'dotenv';

import text from './commands/text';


// configure env vars and client secrets :D
dotenv.config();

const regType = process.argv[2] // args 0 and 1 are `node` and the file name, respectively

const attrsToJSONArray = (list) => {
    ret = [];
    for (item in list) {
        ret.push(item.attribs.toJSON())
    }

    return ret;
}

const allCommands = [
    ...attrsToJSONArray(text),
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
            { body: whichCommands }
        );
        console.log('refreshed commands!');
    }
    catch (error) {
        console.error(error);
    }
};

if (regType === 'clean') {
    registerCommands([]);
}
else if (regType === 'guild') {
    registerCommands(allCommands, false)
}
else {
    registerCommands(allCommands);
}
