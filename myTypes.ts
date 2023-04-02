
import { ChatInputCommandInteraction,  Client, Collection } from 'discord.js';
import { SlashCommandBuilder } from '@discordjs/builders';

export type CommandTuple = {
    attribs: Omit<SlashCommandBuilder, "addSubcommand" | "addSubcommandGroup">,
    execute: (interaction: ChatInputCommandInteraction) => Promise<void>
};

export type CommandCollection = Collection<String, CommandTuple>;
export interface CommandClient extends Client {
    commands: CommandCollection
}
