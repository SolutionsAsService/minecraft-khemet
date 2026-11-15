package dev.shadw.khemet;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BiomeTags;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Blocks;

/** A sandstorm: now and then, for a few minutes, anyone caught in a desert under open sky is slowed and blown with sand. Shelter helps. */
public final class Sandstorm {
	private static boolean active;
	private static long endsAt;

	private Sandstorm() {}

	public static boolean active() {
		return active;
	}

	public static void init() {
		ServerTickEvents.END_WORLD_TICK.register(level -> {
			if (level.dimension() == Level.OVERWORLD) {
				tick(level);
			}
		});
	}

	private static boolean inDesert(ServerLevel level, BlockPos pos) {
		var biome = level.getBiome(pos);
		return biome.is(Biomes.DESERT) || biome.is(BiomeTags.IS_BADLANDS);
	}

	private static void start(ServerLevel level) {
		active = true;
		endsAt = level.getGameTime() + ContentData.i("sandstorm", "duration_seconds") * 20L;
		for (ServerPlayer p : level.players()) {
			if (inDesert(level, p.blockPosition())) {
				p.displayClientMessage(Component.literal("A sandstorm rolls in. Find cover."), false);
			}
		}
	}

	private static void stop(ServerLevel level) {
		active = false;
		for (ServerPlayer p : level.players()) {
			if (inDesert(level, p.blockPosition())) {
				p.displayClientMessage(Component.literal("The sandstorm passes."), false);
			}
		}
	}

	public static int command(CommandSourceStack source, boolean on) {
		ServerLevel level = source.getServer().overworld();
		if (on && !active) {
			start(level);
		} else if (!on && active) {
			stop(level);
		}
		source.sendSuccess(() -> Component.literal(on ? "Sandstorm started." : "Sandstorm stopped."), true);
		return 1;
	}

	private static void tick(ServerLevel level) {
		long time = level.getGameTime();
		if (!active) {
			if (time % 200 == 0 && level.isDay() && !level.isRaining()
					&& level.random.nextInt(ContentData.i("sandstorm", "chance_in")) == 0
					&& level.players().stream().anyMatch(p -> inDesert(level, p.blockPosition()))) {
				start(level);
			}
			return;
		}
		if (time >= endsAt) {
			stop(level);
			return;
		}
		if (time % 20 != 0) {
			return;
		}
		BlockParticleOption sand = new BlockParticleOption(ParticleTypes.FALLING_DUST, Blocks.SAND.defaultBlockState());
		for (ServerPlayer p : level.players()) {
			if (inDesert(level, p.blockPosition()) && level.canSeeSky(p.blockPosition().above())) {
				p.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, ContentData.i("sandstorm", "slowness_amplifier"), true, false));
				level.sendParticles(sand, p.getX() - 3.0, p.getY() + 1.5, p.getZ(), 28, 1.0, 1.2, 4.0, 0.6);
			}
		}
	}
}
