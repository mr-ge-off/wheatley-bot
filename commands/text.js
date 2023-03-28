import { SlashCommandBuilder } from '@discordjs/builders';

const gak = {
    attribs: new SlashCommandBuilder()
        .setName('gak')
        .setDescription('gik!'),
    execute: async (interaction) => {
        await interaction.reply('gik!');
    }
};

const gik = {
    attribs: new SlashCommandBuilder()
    .setName('gik')
    .setDescription('gak!'),
    execute: async (interaction) => {
        await interaction.reply('gik!');
    }
};

const react = {
    attribs: new SlashCommandBuilder()
    .setName('react')
    .setDescription('adds emoji reactions to a post'),
    execute: async (interaction) => {
        await interaction.reply('command pending...');
    }
};

const spongecase = {
    attribs: new SlashCommandBuilder()
    .setName('spongecase')
    .setDescription('turns the text into mocking text'),
    execute: async (interaction) => {
        await interaction.reply('command pending...');
    }
};

const textCommands = [
    gik,
    gak,
    react,
    spongecase
];

export default textCommands;