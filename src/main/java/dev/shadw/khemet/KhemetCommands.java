package dev.shadw.khemet;

import com.google.gson.JsonObject;
import com.mojang.brigadier.arguments.StringArgumentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;

/** /khemet favor shows your standing with each god. The operator commands offer the held item and start or stop a sandstorm. */
public final class KhemetCommands {
	private KhemetCommands() {}

	public static void init() {
		CommandRegistrationCallback.EVENT.register((dispatcher, registryAccess, environment) -> dispatcher.register(
				Commands.literal("khemet")
						.then(Commands.literal("favor").executes(ctx -> favor(ctx.getSource())))
						.then(Commands.literal("offer").requires(src -> src.hasPermission(2))
								.then(Commands.argument("god", StringArgumentType.word())
										.executes(ctx -> offer(ctx.getSource(), StringArgumentType.getString(ctx, "god")))))
						.then(Commands.literal("sandstorm").requires(src -> src.hasPermission(2))
								.then(Commands.literal("start").executes(ctx -> Sandstorm.command(ctx.getSource(), true)))
								.then(Commands.literal("stop").executes(ctx -> Sandstorm.command(ctx.getSource(), false))))));
	}

	private static int favor(CommandSourceStack source) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		ServerPlayer player = source.getPlayerOrException();
		for (String id : KhemetBlocks.GODS) {
			JsonObject god = Favor.god(id);
			int favor = Favor.get(player, id);
			source.sendSuccess(() -> Component.literal(god.get("name").getAsString() + ": favor " + favor + " ("
					+ Favor.stageName(Favor.stage(favor)) + ")"), false);
		}
		return 1;
	}

	private static int offer(CommandSourceStack source, String god) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		if (!java.util.Arrays.asList(KhemetBlocks.GODS).contains(god)) {
			source.sendFailure(Component.literal("Unknown god '" + god + "'. Known: " + String.join(", ", KhemetBlocks.GODS)));
			return 0;
		}
		ServerPlayer player = source.getPlayerOrException();
		boolean accepted = Favor.offer(player, god, player.getMainHandItem());
		int favor = Favor.get(player, god);
		source.sendSuccess(() -> Component.literal((accepted ? "Accepted. " : "Refused. ") + Favor.god(god).get("name").getAsString()
				+ " favor " + favor + " (" + Favor.stageName(Favor.stage(favor)) + ")"), false);
		return accepted ? 1 : 0;
	}
}
