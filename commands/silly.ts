import { EmbedBuilder } from "@discordjs/builders";
import { AttachmentBuilder, ImageURLOptions, SlashCommandBuilder, User } from "discord.js";
import { CommandTuple } from "../myTypes";

const slap: CommandTuple = {
    attribs: new SlashCommandBuilder()
        .setName('slap')
        .setDescription('slaps the target')
        .addUserOption(option =>
            option.setName('target')
                .setDescription('the person to slap')
                .setRequired(true)
        ),
    execute: async interaction => {
        const imageOpts = {
            extension: 'png',
            size: 256
        } as ImageURLOptions;

        const slapper = interaction.user;
        const slappee = interaction.options.getUser('target') as User;

        const slapFile = new AttachmentBuilder('./assets/images/slap.jpg');

        const slapperEmbed = new EmbedBuilder()
            .setImage(slapper.avatarURL(imageOpts));

        const slapEmbed = new EmbedBuilder()
            .setImage('attachment://slap.jpg');

        const slappeeEmbed = new EmbedBuilder()
            .setImage(slappee.avatarURL(imageOpts));

        await interaction.reply(
            {
                embeds: [slapperEmbed, slapEmbed, slappeeEmbed],
                files: [slapFile]
            }
        );
    }
};

const sillyCommands = [
    slap,
];

export default sillyCommands;