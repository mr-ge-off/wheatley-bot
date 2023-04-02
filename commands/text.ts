import { ChatInputCommandInteraction } from 'discord.js';
import { SlashCommandBuilder } from '@discordjs/builders';
import { CommandTuple } from '../myTypes';

const gak: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('gak')
        .setDescription('gik!'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('gik!');
    }
};

const gik: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('gik')
        .setDescription('gak!'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('gak!');
    }
};

const react: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('react')
        .setDescription('adds emoji reactions to a post'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const spongecase: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('spongecase')
        .setDescription('turns the text into mocking text')
        .addStringOption(option => 
            option.setName('text')
                .setDescription('text to mock')
                .setRequired(true)
        ),
    execute: async (interaction: ChatInputCommandInteraction) => {
        let isBig = !!(Math.floor(Math.random() * 2)); // randomize shit
        const words = interaction.options.getString('text')?.split(' ') || [];
        let newWords: string[] = [];
        
        for (const word of words) {
            let newWord = '';
            
            for (const c of word){
                newWord += isBig ? c.toUpperCase() : c.toLowerCase();
                isBig = !isBig;
            }

            newWords.push(newWord);
        }

        await interaction.reply(newWords.join(' '))
    }
};

const textCommands = [
    gik,
    gak,
    react,
    spongecase
];

export default textCommands;