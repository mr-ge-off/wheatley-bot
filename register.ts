import { REST, Routes } from 'discord.js';
import * as dotenv from 'dotenv';

import text from './commands/text';
import voice from './commands/voice';
import silly from './commands/silly';
import admin from './commands/admin';
import { CommandTuple } from './myTypes';

// configure env vars and secrets ;)
dotenv.config();

const regType = process.argv[2] // args 0 and 1 are `node` and the file name, respectively

const attrsToJSONArray = (list: CommandTuple[]) => {
    let ret: any[] = []; // sorry, actual type sucks
    for (const item of list) {
        ret.push(item.attribs.toJSON())
    }

    return ret;
}

const allCommands = [
    ...attrsToJSONArray(text),
    ...attrsToJSONArray(voice),
    ...attrsToJSONArray(silly),
    ...attrsToJSONArray(admin),
];

const registerCommands = async (whichCommands: any[], isGlobal=true) => {
    const restClient = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN as string);

    try {
        console.log('starting command refresh...');
        await restClient.put(
            (isGlobal
                ? Routes.applicationCommands(process.env.APPLICATION_ID as string)
                : Routes.applicationGuildCommands(process.env.APPLICATION_ID as string, process.env.GUILD_ID as string)),
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
