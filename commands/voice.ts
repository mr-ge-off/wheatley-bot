import { ChannelType, ChatInputCommandInteraction, Guild, GuildMember, VoiceChannel } from 'discord.js';
import { SlashCommandBuilder } from '@discordjs/builders';
import { createAudioPlayer, joinVoiceChannel, getVoiceConnection } from "@discordjs/voice";

import { CommandTuple } from '../myTypes';


const EC_ID = '734468488105558026';

const join: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('join')
        .setDescription('I join your voice channel, or one you select')
        .addChannelOption(option =>
            option.setName('channel')
                .setDescription('channel to join')
                .addChannelTypes(ChannelType.GuildVoice)
        ),
    execute: async (interaction: ChatInputCommandInteraction) => {
        const channel = interaction.options.getChannel('channel') as VoiceChannel // get either the paramater channel; or
            || (interaction.member as GuildMember).voice.channel                  // get the channel the user is in; or
            || interaction.guild?.channels.cache.get(EC_ID) as VoiceChannel;      // the Enrichment Center

        joinVoiceChannel({
            channelId: channel.id,
            guildId: channel.guild.id,
            adapterCreator: channel.guild.voiceAdapterCreator
        });

        await interaction.reply(`Joined ${channel}`);
    }
};

const leave: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('leave')
        .setDescription('I leave my voice channel'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        const guildId = interaction.guildId;
        const prevChannel = interaction.channel;
        const connection = guildId ? getVoiceConnection(guildId) : null;

        connection?.disconnect();
        connection?.destroy();

        await interaction.reply(`Left the last channel`);
    }
};

const play: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('play')
        .setDescription('plays a single linked audio blob'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const effect: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('effect')
        .setDescription('plays a sound effect from the list'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const stop: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('stop')
        .setDescription('stops (for good!) the currently playing audio'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const pause: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('pause')
        .setDescription('pauses the currently playing audio'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const resume: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('resume')
        .setDescription('resumes the currently playing audio'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const piss: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('piss')
        .setDescription('I say a rude word'),
    execute: async (interaction: ChatInputCommandInteraction) => {
        await interaction.reply('command pending...');
    }
};

const voiceCommands = [
    join,
    leave,
    play,
    effect,
    pause,
    resume,
    piss,
];

export default voiceCommands;