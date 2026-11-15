package dev.shadw.khemet;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.PushReaction;

/** Egyptian building blocks, two pillars, the sacred brazier, the gods' altars and the river plants. */
public final class KhemetBlocks {
	/** The plain stone variants, in the order they appear in the creative tab. */
	public static final String[] STONES = {"ancient_limestone", "white_limestone", "golden_sandstone", "black_basalt", "polished_pharaoh_stone",
			"hieroglyph_stone", "cracked_temple_stone", "weathered_pyramid_stone", "gold_inlaid_tile", "painted_temple_wall",
			"hieroglyph_bricks", "obelisk_block"};
	public static final String[] GODS = {"ra", "anubis"};

	private static int count;
	public static final List<Block> BUILDING = new ArrayList<>();
	public static final Block[] ALTARS = new Block[GODS.length];

	static {
		for (String name : STONES) {
			BUILDING.add(register(name, key -> new Block(BlockBehaviour.Properties.of().strength(1.5F, 6.0F).sound(SoundType.STONE)
					.requiresCorrectToolForDrops().setId(key))));
		}
	}

	public static final Block GOLDEN_PILLAR = pillar("golden_pillar");
	public static final Block LOTUS_COLUMN = pillar("lotus_column");

	public static final Block SACRED_BRAZIER = register("sacred_brazier", key -> new BrazierBlock(
			BlockBehaviour.Properties.of().strength(2.0F, 6.0F).sound(SoundType.STONE).requiresCorrectToolForDrops()
					.lightLevel(state -> 14).setId(key)));

	public static final Block BLUE_LOTUS = register("blue_lotus", key -> new DesertPlantBlock(MobEffects.NIGHT_VISION, 5.0F,
			BlockBehaviour.Properties.of().noCollission().instabreak().sound(SoundType.GRASS).pushReaction(PushReaction.DESTROY)
					.lightLevel(state -> 3).setId(key)));

	public static final Block PAPYRUS = register("papyrus", key -> new DesertPlantBlock(MobEffects.SATURATION, 4.0F,
			BlockBehaviour.Properties.of().noCollission().instabreak().sound(SoundType.GRASS).pushReaction(PushReaction.DESTROY).setId(key)));

	static {
		BUILDING.add(GOLDEN_PILLAR);
		BUILDING.add(LOTUS_COLUMN);
		for (int i = 0; i < GODS.length; i++) {
			String god = GODS[i];
			ALTARS[i] = register(god + "_altar", key -> new AltarBlock(
					BlockBehaviour.Properties.of().strength(3.0F, 8.0F).sound(SoundType.STONE).requiresCorrectToolForDrops()
							.lightLevel(state -> 7).setId(key), god));
		}
	}

	private KhemetBlocks() {}

	private static Block pillar(String name) {
		return register(name, key -> new RotatedPillarBlock(BlockBehaviour.Properties.of().strength(2.0F, 6.0F).sound(SoundType.STONE)
				.requiresCorrectToolForDrops().setId(key)));
	}

	private static Block register(String path, Function<ResourceKey<Block>, Block> factory) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		Block block = Registry.register(BuiltInRegistries.BLOCK, key, factory.apply(key));
		count++;
		ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, key.location());
		Registry.register(BuiltInRegistries.ITEM, itemKey, new BlockItem(block, new Item.Properties().setId(itemKey).useBlockDescriptionPrefix()));
		return block;
	}

	/** How many blocks this mod registers. */
	public static int count() {
		return count;
	}

	/** Touching this class registers the blocks. */
	public static void init() {}
}
