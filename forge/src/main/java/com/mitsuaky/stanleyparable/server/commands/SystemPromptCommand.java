package com.mitsuaky.stanleyparable.server.commands;

import com.mitsuaky.stanleyparable.events.Event;
import com.mitsuaky.stanleyparable.network.Messages;
import com.mitsuaky.stanleyparable.network.PacketNarrationToClient;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.builder.ArgumentBuilder;
import com.mojang.brigadier.context.CommandContext;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;


public class SystemPromptCommand {
    private static final Logger LOGGER = LogManager.getLogger(SystemPromptCommand.class);

    static ArgumentBuilder<CommandSourceStack, ?> register() {
        return Commands.literal("system")
                .then(Commands.literal("set")
                        .then(
                                Commands.argument("promptID", StringArgumentType.greedyString()).executes(SystemPromptCommand::runCmd)
                        ));
    }

    private static int runCmd(CommandContext<CommandSourceStack> ctx) {
        LOGGER.debug("Set system prompt command triggered");

        ServerPlayer player = ctx.getSource().getPlayer();
        String msg = StringArgumentType.getString(ctx, "promptID");
        String event = Event.SET_SYSTEM.getValue();
        Messages.sendToPlayer(new PacketNarrationToClient(event, msg), player);

        ctx.getSource().sendSuccess(() -> Component.literal("Sent to backend"), false);
        return 1;
    }
}