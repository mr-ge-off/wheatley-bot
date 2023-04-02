import { PermissionFlagsBits, SlashCommandBuilder, Snowflake, User } from "discord.js";
import { CommandTuple } from "../myTypes";

export let lockUserInstance: User | null;

const lock: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('lock')
        .setDescription('locks me to only listen to one user')
        .addUserOption(option => 
            option.setName('user')
            .setDescription('the user to lock to, if not you')
        )
        .setDefaultMemberPermissions(PermissionFlagsBits.Administrator),
    execute: async interaction => {
        if (lockUserInstance) {
            await interaction.reply({
                content: `I'm already locked to ${lockUserInstance}`,
                ephemeral: true,
                target: interaction.user
            });
        }
        else {
            lockUserInstance = interaction.options.getUser('user') ?? interaction.user;
            await interaction.reply(`I'm now locked to ${lockUserInstance}`);
        }
    }
}   

const unlock: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('unlock')
        .setDescription('unlocks me if I am locked to a user')
        .setDefaultMemberPermissions(PermissionFlagsBits.Administrator),
    execute: async interaction => {
        if (!lockUserInstance) {
            await interaction.reply({
                content: "I'm not currently locked",
                ephemeral: true,
                target: interaction.user
            });

            return;
        }
        
        lockUserInstance = null;
        await interaction.reply("I'm now unlocked");
    }
}

const adminCommands = [
    lock,
    unlock,
];

export default adminCommands;